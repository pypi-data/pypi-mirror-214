"""Bare-bones Python package to access G4Edge test data files."""
from __future__ import annotations

from g4edgetestdata._version import version as __version__
from g4edgetestdata.core import G4EdgeTestData

__all__ = ["__version__", "G4EdgeTestData"]
