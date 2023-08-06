from __future__ import annotations

import logging
import os
from getpass import getuser
from pathlib import Path
from tempfile import gettempdir

from git import GitCommandError, InvalidGitRepositoryError, Repo

log = logging.getLogger(__name__)


class G4EdgeTestData:
    def __init__(self):
        self._default_git_ref = "main"
        self._repo_path = Path(
            os.getenv("G4EDGE_TESTDATA", gettempdir() + "/g4edge-testdata-" + getuser())
        )
        self._repo: Repo = self._init_testdata_repo()

    def _init_testdata_repo(self) -> None:
        if not self._repo_path.is_dir():
            self._repo_path.mkdir()

        repo = None
        try:
            repo = Repo(self._repo_path)
        except InvalidGitRepositoryError:
            log.info(
                "Cloning https://github.com/g4edge/testdata in %s...",
                str(self._repo_path),
            )
            repo = Repo.clone_from(
                "https://github.com/g4edge/testdata", self._repo_path
            )

        repo.git.checkout(self._default_git_ref)

        return repo

    def checkout(self, git_ref: str) -> None:
        try:
            self._repo.git.checkout(git_ref)
        except GitCommandError:
            self._repo.remote().pull()
            self._repo.git.checkout(git_ref)

    def reset(self) -> None:
        self._repo.git.checkout(self._default_git_ref)

    def __getitem__(self, filename: str | Path) -> Path:
        """Get an absolute path to a G4Edge test data file.

        Parameters
        ----------
        filename : str
            path of the file relative to g4edge/testdata/data
        """
        full_path = (self._repo_path / "data" / filename).resolve()

        if not full_path.exists():
            msg = f'Test file/directory "{filename}" not found in g4edge/testdata repository'
            raise FileNotFoundError(msg)

        return full_path
