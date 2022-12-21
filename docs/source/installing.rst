.. _installing:

Installation
============

How to install nctoolkit
---------------------

You will need a Linux or Mac operating system for nctoolkit to work. It will not work on Windows due to system requirements. 

The best and easiest way to install nctoolkit is to use conda. This will install all system dependencies, and nctoolkit will just work out of the box. This can be done as follows::

   $ conda install -c conda-forge nctoolkit

Mamba is a smoother way to manage conda environments. If you don't use it, you should try. Install it from  `here  <https://github.com/conda-forge/miniforge/>`__.

Once mambaforge is installed you can install nctoolkit as follows::

   $ mamba install -c conda-forge nctoolkit

This will be much faster to install than using conda, because mamba resolves environments much faster.

Note that recent releases are not available on macOS on conda. This issue is being investigated at the minute, and will hopefully be resolved shortly. In the meantime, if you are using macOS, it is best to install using pip.

If you do not use conda, you can install nctoolkit using pip. The package is available from the `Python Packaging Index. <https://pypi.org/project/nctoolkit/>`__   To install nctoolkit using pip::

   $ pip install nctoolkit 

nctoolkit partly relies on cartopy for plotting. This has some additional dependencies, so you may need to follow their guide `here <https://pypi.org/project/nctoolkit/>`__ to ensure cartopy is installed fully. If you install nctoolkit using conda, you will not need to worry about that.

Once you have installed nctoolkit using pip, you will need to install the system dependencies listed below.

To install the development version from GitHub::

   $ pip install git+https://github.com/r4ecology/nctoolkit.git



Python dependencies
---------------------

- Python (3.6 or later)
- `numpy <http://www.numpy.org/>`__ (1.14 or later)
- `pandas <http://pandas.pydata.org/>`__ (0.24 or later)
- `xarray <http://xarray.pydata.org/en/stable/>`__ (0.14 or later)
- `netCDF4 <https://unidata.github.io/netCDF4-python/netCDF4/index.html>`__ (1.53 or later)
- `ncplot <https://ncplot.readthedocs.io/en/stable/>`__ 


System dependencies
---------------------
There are two main system dependencies: `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/wiki>`__, and `NCO <http://nco.sourceforge.net/>`__. The easiest way to install them is using conda::

    $ conda install -c conda-forge cdo

    $ conda install -c conda-forge nco

or mamba::

    $ mamba install -c conda-forge cdo

    $ mamba install -c conda-forge nco

CDO is necessary for the package to work. NCO is an optional dependency and does not have to be installed.

If you are working on an Ubuntu system, you should be able to install CDO as follows::

    $ sudo apt install cdo 


If you want to install CDO from source, you can use one of the bash scripts available `here. <https://github.com/r4ecology/nctoolkit/tree/master/cdo_installers>`__












