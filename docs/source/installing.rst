.. _installing:

Installation
============

How to install nctoolkit
---------------------

You will need a Linux or Mac operating system for nctoolkit to work. It will not work on Windows due to system requirements. 

nctoolkit is available from the `Python Packaging Index. <https://pypi.org/project/nctoolkit/>`__   To install nctoolkit using pip::

   $ pip install numpy 
   $ pip install nctoolkit 

If you already have numpy installed, ignore the first line. This is only included as it will make installing some dependencies smoother. nctoolkit partly relies on cartopy for plotting. This has some additional dependencies, so you may need to follow their guide `here <https://pypi.org/project/nctoolkit/>`__ to ensure cartopy is installed fully. If you install nctoolkit using conda, you will not need to worry about that.

If you install nctoolkit from pypi, you will need to install the system dependencies listed below.

nctoolkit can also be installed using conda, as follows::

   $ conda install -c conda-forge nctoolkit

Note that recent releases are not available for Python 3.8 on macOS on conda. This issue is being investigated at the minute, and will hopefully be resolved shortly. In the meantime, if you are using macOS and Python 3.8, it is best to install using pip.

At present this can be slow due to the time taken to resolve dependency versions. If you run into problems just use pip. 

To install the development version from GitHub::

   $ pip install git+https://github.com/r4ecology/nctoolkit.git

Plotting issue
---------------------

An update to a dependency of a dependency has broken plotting in nctoolkit, unless you have ncplot version 0.2.4 installed. If you experience an error related to jinja2, downgrade the package as follows::

        $ conda install jinja2=3.0.3 
        $ pip install jinja2==3.0.3


Or install the latest version of ncplot::

        $ conda install ncplot=0.2.4 
        $ pip install ncplot==0.2.4

Jupyter notebook issue
---------------------

A recent update to ipykernel has broken some functionality in jupyter notebooks, with Python not exiting properly when notebooks are restarted or closed. This is resulting in nctoolkit not automatically deleting temporary files at the end of sessions. To fix this just downgrade ipykernel::

        $ conda install ipykernel=6.9.1
        $ pip install ipykernel==6.9.1



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


CDO is necessary for the package to work. NCO is an optional dependency and does not have to be installed.

If you are working on an Ubuntu system, you should be able to install CDO as follows::

    $ sudo apt install cdo 


If you want to install CDO from source, you can use one of the bash scripts available `here. <https://github.com/r4ecology/nctoolkit/tree/master/cdo_installers>`__












