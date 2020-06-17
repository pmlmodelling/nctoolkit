.. _installing:

Installation
============

Python dependencies
---------------------

- Python (3.6 or later)
- `numpy <http://www.numpy.org/>`__ (1.14 or later)
- `pandas <http://pandas.pydata.org/>`__ (0.24 or later)
- `xarray <http://xarray.pydata.org/en/stable/>`__ (0.14 or later)
- `hvplot <https://hvplot.holoviz.org/>`__ (0.5 or later)
- `NetCDF4 <https://unidata.github.io/NetCDF4-python/NetCDF4/index.html>`__ (1.53 or later)
- `panel <https://panel.holoviz.org/>`__ (0.9.1 or later)



System dependencies
---------------------
There are two main system dependencies: `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/wiki>`__, and `NCO <http://nco.sourceforge.net/>`__. The easiest way to install them is using conda::

    $ conda install -c conda-forge cdo

    $ conda install -c conda-forge nco


While CDO is necessary for the package to work, NCO is an optional dependency.

If you want to install CDO from source with NetCDF and HDF5 support, you can use one of the bash scripts available `here. <https://github.com/r4ecology/nctoolkit/tree/master/cdo_installers>`__



How to install nctoolkit
---------------------

nctoolkit is available from the `Python Packaging Index. <https://pypi.org/project/nctoolkit/>`__   To install nctoolkit using pip::

   $ pip install nctoolkit 

To install the development version from GitHub::

   $ pip install git+https://github.com/r4ecology/nctoolkit.git









