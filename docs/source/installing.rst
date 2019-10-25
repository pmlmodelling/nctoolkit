.. _installing:

Installation
============

Python dependencies
---------------------

- Python (2.7 or later)
- `numpy <http://www.numpy.org/>`__ (1.14 or later)
- `pandas <http://pandas.pydata.org/>`__ (0.24 or later)
- `xarray <http://xarray.pydata.org/en/stable/>`__ (0.14 or later)


System dependencies
---------------------
**Climate Data Operators**. This can either be installed from source at the `CDO website <https://code.mpimet.mpg.de/projects/cdo/wiki>`, or it can be installed from system repositories. For example, in Ubuntu you can install CDO as follows::

   $ sudo apt-get install cdo

At present, nchack is set up to use the "vanilla" version fo CDO, so it will not be able to utilize parallel processing of files using.

**NCO**. This can either be installed from source at the `NCO website <http://nco.sourceforge.net/>`, or it can be installed from system repositories. For example, in Ubuntu you can install NCO as follows::

   $ sudo apt-get install nco

**Netcdf4** and **HDF5**. If your system is not presently set up to work with netcdf files, you will need to install Netcdf4 and HDF5. How this is done will vary by system, however there are easily available guides online (for example, `here <http://www.studytrails.com/blog/install-climate-data-operator-cdo-with-netcdf-grib2-and-hdf5-support/>` and `here <https://gist.github.com/danwild/d7225afe4b7dbdeeb87982f0e71012f3>`.


How to install nchack
---------------------

To install the development version of nchack::

   $ pip install git+https://github.com/r4ecology/nchack.git







