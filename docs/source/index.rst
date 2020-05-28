
nctoolkit: tools to manipulate and analyze NetCDF data in Python
=======================================================

The goal of nctoolkit is to provide a comprehensive tool in Python for manipulating NetCDF data. The philosophy is to provide sufficient methods to carry out 80-90% of what you want to do with NetCDF files.

nctoolkit is designed with both individual files and ensembles in mind. 

Under the hood nctoolkit relies on the command line packages Climate Data Operates (CDO), with NCO as an optional dependency. No prior knowledge of CDO is required to use nctoolkit. 

The package is design with two uses in mind: computationally intensive data post-processing and interactive Jupyter notebook type analysis. An auto plotting feature is provided to aid rapid data analysis.

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
   



















