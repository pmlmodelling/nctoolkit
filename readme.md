
<!-- README.md is generated from README.Rmd. Please edit that file -->

## Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)


# nchack - easy tools for manipulating netcdf data in Python

The goal of nchack is to provide a comprehensive tool in Python for manipulating individual netcdf files and ensembles of netcdf files. The philosophy is to provide sufficient methods to carry out 80-90% of netcdf manipulations.

This package will work with Python 3.6 upwards.

## Installation


You can install the development version of nchack using using pip as follows.
```sh
pip install git+https://github.com/r4ecology/nchack.git
```

This package relies on CDO and NCO under the hood.
Visit <https://code.mpimet.mpg.de/projects/cdo/files> for CDO download and
installation instructions. Note that the development version is
currently tested using CDO Version 1.9.7. Vist http://nco.sourceforge.net/ to download and install NCO.

If you use Anaconda, you can install these packages as follows:

```sh
conda install -c conda-forge cdo 
```
```sh
conda install -c conda-forge nco 
```
 
Currently, the package has been tested for Linux computers. It will not
work on Windows platforms, currently. But (buyer beware) it should work on Macs.

## Reference and tutorials

A full API reference, in depth tutorials and a how-to guide are available at [readthedocs](https://nchack.readthedocs.io/en/latest/).


