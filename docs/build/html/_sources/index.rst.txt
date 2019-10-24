
nchack: tools to manipulate and analyze netcdf data in Python
=======================================================

The goal of nchack is to provide a comprehensive tool in Python for manipulating individual netcdf files and ensembles of netcdf files. The philosophy is to provide sufficient methods to carry out 80-90% of what you want to do with netcdf files.

nchack is designed with both individual files and ensembles in mind. 

Under the hood nchack relies on the command line packages Climate Data Operates (CDO) and the NCO toolkit, but primarily on CDO. No prioer knowledge of CDO or NCO are required to use nchack. Behind the scenes nchack will generate system calls to either CDO or NCO, which are traced and can be viewed by the user. However, in almost all cases these can be ignored by most users.


Documentation
-------------
**Getting Started**

* :doc:`tutorial`
* :doc:`installing`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started

   installing
   basic_usage
   lazy_methods 
   merging_notebook 

**User Guide**


**Help & reference**

* :doc:`api`
* :doc:`backends`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help & reference

   howto
   api
   backends
   















