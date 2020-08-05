
nctoolkit: Efficient and intuitive tools for analyzing netCDF data in Python 
=======================================================

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

Under the hood nctoolkit relies on Climate Data Operators (CDO). nctoolkit is designed as a standalone package with no required understanding of CDO, but it provides expert users of CDO the ability to process data in Python with ease, and with method chaining handled automatically.

In addition to the guidance given here, tutorials for how to use nctoolkit are available at nctoolkit's `GitHub page. <https://github.com/r4ecology/nctoolkit/tree/master/tutorials>`__


Documentation
-------------
**Getting Started**

* :doc:`installing`
* :doc:`basic_usage`
* :doc:`merging_notebook`
* :doc:`lazy_methods`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   installing
   basic_usage
   merging_notebook 
   lazy_methods 

**User Guide**


**Help & reference**

* :doc:`a_to_z`
* :doc:`api`
* :doc:`howto`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & reference

   a_to_z
   howto
   api
   



















