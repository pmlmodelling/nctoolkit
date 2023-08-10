
<!-- README.md is generated from README.Rmd. Please edit that file -->

[![pypi](https://img.shields.io/pypi/v/nctoolkit.svg)](https://pypi.python.org/pypi/nctoolkit/)
[![Conda Latest Release](https://anaconda.org/conda-forge/nctoolkit/badges/version.svg)](https://anaconda.org/conda-forge/nctoolkit/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pmlmodelling/nctoolkit/issues) 
[![codecov](https://codecov.io/gh/pmlmodelling/nctoolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/pmlmodelling/nctoolkit)
![GitHub Testing](https://github.com/pmlmodelling/nctoolkit/actions/workflows/python-app-macos.yml/badge.svg)
![GitHub Testing](https://github.com/pmlmodelling/nctoolkit/actions/workflows/python-app-linux.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nctoolkit/badge/?version=latest)](https://nctoolkit.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.05494/status.svg)](https://doi.org/10.21105/joss.05494)






# nctoolkit - A Python package for netCDF analysis and post-processing 

nctoolkit is a comprehensive Python (3.8 and above) package for analyzing netCDF data on Linux and macOS.

Core abilities include:
   - Clipping to spatial regions
   - Calculating climatologies
   - Subsetting to specific time periods
   - Calculating spatial statistics
   - Creating new variables using arithmetic operations
   - Calculating anomalies
   - Calculating rolling and cumulative statistics
   - Horizontally and vertically remapping data
   - Calculating time averages
   - Interactive plotting of data
   - Calculating the correlations between variables
   - Calculating vertical statistics for the likes of oceanic data
   - Calculating ensemble statistics
   - Calculating phenological metrics

[![PML logo](docs/source/pml-logo.gif)](https://pml.ac.uk/)


## Installation

The easiest way to install the package is using conda or mamba. This will install nctoolkit and all system dependencies.
```sh
conda install -c conda-forge nctoolkit
mamba install -c conda-forge nctoolkit
```

If you install using conda, please be aware that conda can install a very old version of nctoolkit. Consider setting it to a more recent version.

Install through [PyPI](https://pypi.org/project/nctoolkit/) using pip:
```sh
pip install nctoolkit 
```

Install the development version using using pip:
```sh
pip install git+https://github.com/pmlmodelling/nctoolkit.git
```

This package requires the installation of [Climate Data Operators](https://code.mpimet.mpg.de/projects/cdo/wiki). The conda installation will handle this for you. Otherwise, you will have to install it.  The easiest way is using conda:

```sh
conda install -c conda-forge cdo 
```

A couple of methods give users the option of using [NetCDF Operators](http://nco.sourceforge.net/) instead of CDO as the computational backend. Again, the easiest way to install is using conda:

```sh
conda install -c conda-forge nco 
```

If you want to install CDO from source, bash scripts are available [here](https://github.com/pmlmodelling/nctoolkit/tree/master/cdo_installers).
 
nctoolkit is tested with continuous integration using Circle CI (for Linux) and GitHub actions (for Mac OS). It will not work on Windows platforms today or in future, because of system dependency limitations. 


## Reference and tutorials

A full API reference, in depth tutorials and a how-to guide are available at [readthedocs](https://nctoolkit.readthedocs.io/en/latest/).



## Contributing

If you are interesting in contributing to nctoolkit feel free to read the [Contributing page](https://nctoolkit.readthedocs.io/en/latest/contributing.html).

## Got questions about nctoolkit? 

- If you have a question about how to use nctoolkit, please ask on 
    [GitHub Discussions](https://github.com/pmlmodelling/nctoolkit/discussions).
- Report any bugs, suggest new features or view the source code [on
    GitHub](https://github.com/pmlmodelling/nctoolkit).

















