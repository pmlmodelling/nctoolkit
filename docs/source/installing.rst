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



System dependencies
---------------------
There are two main system dependencies: `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/wiki>`__, and `NCO <http://nco.sourceforge.net/>`__. The easiest way to install them is using conda. This method will also ensure that the hdf5 libraries are threadsafe, which can lead to computational improvements using CDO:

    $ conda install -c conda-forge cdo

    $ conda install -c conda-forge nco



How to install nctoolkit
---------------------

To install the development version of nctoolkit::

   $ pip install git+https://github.com/r4ecology/nctoolkit.git









