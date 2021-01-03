
nctoolkit: Fast and easy analysis of netCDF data in Python 
=======================================================

nctoolkit is a comprehensive Python package for analyzing netCDF data on Linux and MacOS.

Core abilities include:

   - Cropping to geographic regions
   - Interactive plotting of data
   - Subsetting to specific time periods
   - Calculating time averages
   - Calculating spatial averages
   - Calculating rolling averages
   - Calculating climatologies
   - Creating new variables using arithmetic operations
   - Calculating anomalies
   - Horizontally and vertically remapping data
   - Calculating the correlations between variables
   - Calculating vertical averages for the likes of oceanic data
   - Calculating ensemble averages
   - Calculating phenological metrics


Fixing plotting problem due to xarray bug
---------------------

There is currently a bug in xarray caused by the update of pandas to version 1.1. As a result some plots will fail in nctoolkit. To fix this ensure pandas version 1.0.5 is installed. Do this after installing nctoolkit. This can be done as follows::


   $ conda install -c conda-forge pandas=1.0.5 

or::

   $ pip install pandas==1.0.5




Documentation
-------------
**Quick overview**

* :doc:`installing`
* :doc:`basic_usage`
* :doc:`merging_notebook`
* :doc:`lazy_methods`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Quick overview 

   installing
   basic_usage

**User Guide**

* :doc:`datasets`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: User Guide 

   datasets
   exporting 
   subsetting 
   temporals 
   merging_notebook 
   lazy_methods 


**Reference and help**

* :doc:`a_to_z`
* :doc:`api`
* :doc:`howto`
* :doc:`info`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference & help

   a_to_z
   howto
   api
   info
   



















