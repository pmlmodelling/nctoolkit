
<!-- README.md is generated from README.Rmd. Please edit that file -->

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/r4ecology/nctoolkit/issues) 
[![codecov](https://codecov.io/gh/r4ecology/nctoolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/r4ecology/nctoolkit)
[![Build Status](https://travis-ci.org/r4ecology/nctoolkit.png?branch=master)](https://travis-ci.org/r4ecology/nctoolkit)
[![Documentation Status](https://readthedocs.org/projects/nctoolkit/badge/?version=latest)](https://nctoolkit.readthedocs.io/en/latest/?badge=latest)





# nctoolkit - Efficient and intuitive tools for analyzing netCDF data in Python


nctoolkit is a comprehensive Python (3.6 and above) package for analyzing netCDF data.

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

## Installation

The easiest way to install the package is using conda. This will install nctoolkit and all system dependencies.
```sh
conda install -c rwi nctoolkit
```

Install through [PyPI](https://pypi.org/project/nctoolkit/) using pip:
```sh
pip install nctoolkit 
```

Install the development version using using pip:
```sh
pip install git+https://github.com/r4ecology/nctoolkit.git
```

This package requires the installation of [Climate Data Operators](https://code.mpimet.mpg.de/projects/cdo/wiki). The conda installation will handle this for you. Otherwise, you will have to install it.  The easiest way is using conda:

```sh
conda install -c conda-forge cdo 
```

A couple of methods give users the option of using [NetCDF Operators](http://nco.sourceforge.net/) instead of CDO as the computational backend. Again, the easiest way to install is using conda:

```sh
conda install -c conda-forge nco 
```

If you want to install CDO from source, bash scripts are available [here](https://github.com/r4ecology/nctoolkit/tree/master/cdo_installers).
 
The package has been tested thoroughly for Linux, with continuous integration using Travis. It will not work on Windows platforms, but might in future version. It is untested on Mac operating systems, so should be used cautiously on them.






## Reference and tutorials

A full API reference, in depth tutorials and a how-to guide are available at [readthedocs](https://nctoolkit.readthedocs.io/en/latest/).



















