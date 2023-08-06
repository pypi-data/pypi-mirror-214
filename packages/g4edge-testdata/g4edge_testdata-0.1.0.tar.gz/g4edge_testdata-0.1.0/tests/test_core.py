from __future__ import annotations

import pytest
from git import GitCommandError

from g4edgetestdata import G4EdgeTestData

g4data = G4EdgeTestData()
g4data.checkout("4bfcae3")


def test_get_file():
    g4data["gdml/001_box.gdml"]


def test_get_directory():
    g4data["gdml"]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        g4data["non-existing-file.ext"]


def test_git_ref_not_found():
    with pytest.raises(GitCommandError):
        g4data.checkout("non-existent-ref")
