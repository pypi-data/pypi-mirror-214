use liboxen::model::entry::mod_entry::ModType;
use pyo3::prelude::*;

use liboxen::config::UserConfig;
use liboxen::model::{CommitBody, ContentType, Remote, RemoteRepository};
use liboxen::{api, command};

use pyo3::exceptions::PyValueError;
use std::path::PathBuf;

use crate::error::PyOxenError;
use crate::py_branch::PyBranch;
use crate::py_commit::PyCommit;

use crate::py_staged_data::PyStagedData;

#[pyclass]
pub struct PyRemoteRepo {
    repo: RemoteRepository,
    host: String,
    #[pyo3(get)]
    revision: String,
}

#[pymethods]
impl PyRemoteRepo {
    #[new]
    #[pyo3(signature = (repo, host, revision))]
    fn py_new(repo: String, host: String, revision: String) -> PyResult<Self> {
        let (namespace, repo_name) = match repo.split_once('/') {
            Some((namespace, repo_name)) => (namespace.to_string(), repo_name.to_string()),
            None => {
                return Err(PyValueError::new_err(
                    "Invalid repo name, must be in format namespace/repo_name",
                ))
            }
        };

        Ok(Self {
            repo: RemoteRepository {
                namespace: namespace.to_owned(),
                name: repo_name.to_owned(),
                remote: Remote {
                    url: liboxen::api::endpoint::remote_url_from_host(
                        &host, &namespace, &repo_name,
                    ),
                    name: String::from(liboxen::constants::DEFAULT_REMOTE_NAME),
                },
            },
            host,
            revision,
        })
    }

    fn url(&self) -> &str {
        self.repo.url()
    }

    fn namespace(&self) -> &str {
        &self.repo.namespace
    }

    fn name(&self) -> &str {
        &self.repo.name
    }

    fn revision(&self) -> &str {
        &self.revision
    }

    fn set_revision(&mut self, new_revision: String) {
        self.revision = new_revision;
    }

    fn create(&mut self) -> Result<PyRemoteRepo, PyOxenError> {
        let result = pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::repositories::create_no_root(
                &self.repo.namespace,
                &self.repo.name,
                &self.host,
            )
            .await
        })?;

        self.repo = result;

        Ok(PyRemoteRepo {
            repo: self.repo.clone(),
            host: self.host.clone(),
            revision: self.revision.clone(),
        })
    }

    fn exists(&self) -> Result<bool, PyOxenError> {
        let exists = pyo3_asyncio::tokio::get_runtime()
            .block_on(async { api::remote::repositories::exists(&self.repo).await })?;

        Ok(exists)
    }

    fn delete(&self) -> Result<(), PyOxenError> {
        pyo3_asyncio::tokio::get_runtime()
            .block_on(async { api::remote::repositories::delete(&self.repo).await })?;

        Ok(())
    }

    fn download(&self, remote_path: PathBuf, local_path: PathBuf) -> Result<(), PyOxenError> {
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            command::remote::download(&self.repo, &remote_path, &local_path, &self.revision).await
        })?;

        Ok(())
    }

    fn add(&self, directory_name: String, path: PathBuf) -> Result<(), PyOxenError> {
        let user_id = UserConfig::identifier()?;
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::add_file(
                &self.repo,
                &self.revision,
                &user_id,
                &directory_name,
                path,
            )
            .await
        })?;
        Ok(())
    }

    fn remove(&self, path: PathBuf) -> Result<(), PyOxenError> {
        let user_id = UserConfig::identifier()?;
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::rm_staged_file(&self.repo, &self.revision, &user_id, path).await
        })?;
        Ok(())
    }

    fn commit(&self, message: String) -> Result<(), PyOxenError> {
        let user_id = UserConfig::identifier()?;
        let user = UserConfig::get()?.to_user();
        let commit = CommitBody { message, user };
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::commit_staged(&self.repo, &self.revision, &user_id, &commit).await
        })?;
        Ok(())
    }

    fn log(&self) -> Result<Vec<PyCommit>, PyOxenError> {
        let log = pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::commits::list_commit_history(&self.repo, &self.revision).await
        })?;
        Ok(log.iter().map(|c| PyCommit { commit: c.clone() }).collect())
    }

    fn add_df_row(&self, path: PathBuf, data: String) -> Result<(), PyOxenError> {
        let user_id = UserConfig::identifier()?;
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::stage_modification(
                &self.repo,
                &self.revision,
                &user_id,
                &path,
                data,
                ContentType::Json,
                ModType::Append,
            )
            .await
        })?;
        Ok(())
    }

    fn restore_df(&self, path: PathBuf) -> Result<(), PyOxenError> {
        let user_id = UserConfig::identifier()?;
        pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::restore_df(&self.repo, &self.revision, &user_id, &path).await
        })?;
        Ok(())
    }

    fn list_branches(&self) -> Result<Vec<PyBranch>, PyOxenError> {
        let branches = pyo3_asyncio::tokio::get_runtime()
            .block_on(async { api::remote::branches::list(&self.repo).await })?;
        Ok(branches
            .iter()
            .map(|b| PyBranch::new(b.name.clone(), b.commit_id.clone(), false))
            .collect())
    }

    fn status(&self, path: PathBuf) -> Result<PyStagedData, PyOxenError> {
        let user_id = UserConfig::identifier()?;
        let remote_status = pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::staging::status(
                &self.repo,
                &self.revision,
                &user_id,
                &path,
                liboxen::constants::DEFAULT_PAGE_NUM,
                liboxen::constants::DEFAULT_PAGE_SIZE,
            )
            .await
        })?;

        // Convert remote status to a PyStagedData using the from method
        Ok(PyStagedData::from(remote_status))
    }

    fn get_branch(&self, branch_name: String) -> PyResult<PyBranch> {
        log::info!("Get branch... {branch_name}");

        let branch = pyo3_asyncio::tokio::get_runtime().block_on(async {
            log::info!("From repo... {}", self.repo.remote.url);
            api::remote::branches::get_by_name(&self.repo, &branch_name).await
        });

        match branch {
            Ok(Some(branch)) => Ok(PyBranch::from(branch)),
            _ => Err(PyValueError::new_err("could not get branch")),
        }
    }

    fn get_commit(&self, commit_id: String) -> PyResult<PyCommit> {
        let commit = pyo3_asyncio::tokio::get_runtime()
            .block_on(async { api::remote::commits::get_by_id(&self.repo, &commit_id).await });
        match commit {
            Ok(Some(commit)) => Ok(PyCommit { commit }),
            _ => Err(PyValueError::new_err("could not get commit id {commit_id}")),
        }
    }

    fn create_branch(&self, new_name: String) -> PyResult<PyBranch> {
        let branch = pyo3_asyncio::tokio::get_runtime().block_on(async {
            api::remote::branches::create_from_or_get(&self.repo, &new_name, &self.revision).await
        });

        match branch {
            Ok(branch) => Ok(PyBranch::from(branch)),
            _ => Err(PyValueError::new_err("Could not get or create branch")),
        }
    }
    fn checkout(&mut self, revision: String) -> PyResult<()> {
        let branch = self.get_branch(revision.clone());
        if let Ok(branch) = branch {
            self.set_revision(branch.name().to_string());
            return Ok(());
        }

        let commit = self.get_commit(revision.clone());
        match commit {
            Ok(commit) => {
                self.set_revision(commit.commit.id);
                Ok(())
            },
            _ => Err(PyValueError::new_err(format!("{} is not a valid branch name or commit id. Consider creating it with `create_branch`", revision)))
        }
    }
}
