.. _installing:

Installation
============

Python dependencies
---------------------

- Python (3.6 or later)
- `numpy <http://www.numpy.org/>`__ (1.14 or later)
- `pandas <http://pandas.pydata.org/>`__ (0.24 or later)
- `xarray <http://xarray.pydata.org/en/stable/>`__ (0.14 or later)
- `NetCDF4 <https://unidata.github.io/NetCDF4-python/NetCDF4/index.html>`__ (1.53 or later)
- `hvplot <https://ncplot.readthedocs.io/en/stable/>`__ 

How to install nctoolkit
---------------------

The easiest way to install the package is using conda, which will install nctoolkit and all system dependencies::

   $ conda install -c conda-forge nctoolkit

nctoolkit is available from the `Python Packaging Index. <https://pypi.org/project/nctoolkit/>`__   To install nctoolkit using pip::

   $ pip install nctoolkit 

If you install nctoolkit from pypi, you will need to install the system dependencies listed below.

To install the development version from GitHub::

   $ pip install git+https://github.com/r4ecology/nctoolkit.git


System dependencies
---------------------
There are two main system dependencies: `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/wiki>`__, and `NCO <http://nco.sourceforge.net/>`__. The easiest way to install them is using conda::

    $ conda install -c conda-forge cdo

    $ conda install -c conda-forge nco


CDO is necessary for the package to work. NCO is an optional dependency and does not have to be installed.

If you want to install CDO from source, you can use one of the bash scripts available `here. <https://github.com/r4ecology/nctoolkit/tree/master/cdo_installers>`__












