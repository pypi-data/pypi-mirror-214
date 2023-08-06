# g4edge test data

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/g4edge/testdata?logo=git)
[![GitHub Workflow Status](https://img.shields.io/github/checks-status/g4edge/testdata/main?label=main%20branch&logo=github)](https://github.com/g4edge/testdata/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub issues](https://img.shields.io/github/issues/g4edge/testdata?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr/g4edge/testdata?logo=github)
![License](https://img.shields.io/github/license/g4edge/testdata)

Install (with pip):

```console
$ python -m pip install g4edge-testdata
```

### Usage

Instantiating a `G4EdgeTestData` object:

```python
from g4edgetestdata import G4EdgeTestData

g4data = G4EdgeTestData()
```

Clones [g4edge/testdata](https://github.com/g4edge/testdata) in a temporary
location (not preserved across system reboots), unless the environment variable
`G4EDGE_TESTDATA` is set and points to the location of an existing
g4edge/testdata clone.

Alternatively, the path to an existing g4edge/testdata clone can be provided to
the class constructor:

```python
from g4edgetestdata import G4EdgeTestData

g4data = G4EdgeTestData("path/to/g4edge/testdata")
```

Access to data files is provided through the square brackets operator:

```pycon
>>> g4data["gdml/001_box.gdml"]
PosixPath('/tmp/g4edge-testdata-gipert/data/gdml/001_box.gdml')
```
