
nctoolkit: tools to manipulate and analyze NetCDF data in Python
=======================================================

The goal of nctoolkit is to provide a comprehensive tool in Python for manipulating individual NetCDF files and ensembles of NetCDF files. The philosophy is to provide sufficient methods to carry out 80-90% of what you want to do with NetCDF files.

nctoolkit is designed with both individual files and ensembles in mind. 

Under the hood nctoolkit relies on the command line packages Climate Data Operates (CDO) and the NCO toolkit, but primarily on CDO. No prior knowledge of CDO or NCO are required to use nctoolkit. Behind the scenes, nctoolkit will generate system calls to either CDO or NCO, which are traced and can be viewed by the user. However, in almost all cases these can be ignored by most users.


Documentation
-------------
**Getting Started**

* :doc:`installing`

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

* :doc:`api`
* :doc:`howto`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & reference

   howto
   api
   



















