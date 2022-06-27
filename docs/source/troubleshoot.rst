Toubleshooting
============

If you get errors running nctoolkit these are most likely caused by problems in the data. In some cases these can be fixed. The tips below will point you help you do this. 

Check data types
---------------

Under-the-hood, nctoolkit uses Climate Data Operators (CDO) as its computational engine. By default, CDO uses the data type stored in netCDF files. In most cases, this will not cause
any problems. However, some times it will. For example, imagine you want to calculate the fraction of time temperature exceeds 30 degrees, but the data is stored as integer format. In nctoolkit, you could
calculate this as follows:


.. code:: ipython3
   ds.assign(temperature = lambda x: x.temperature > 30)
   ds.tmean()

In theory, this is fine. But, if the data is stored as integer format, you will end up either with 0 or 1 in the data. Instead we want to change the numerical precision of the data. We could do this as
follows:

.. code:: ipython3
   ds.set_precision("F64")
   ds.assign(temperature = lambda x: x.temperature > 30)
   ds.tmean()

By default, nctoolkit will warn you if a dataset has integer data types when you open a dataset. But if you want to know what data types each variable has just do the following:

.. code:: ipython3
   ds.contents

How to carry out general checks on a dataset
---------------

There is a built in method in nctoolkit for checking if the format of a dataset is problematic. Just do the following:

.. code:: ipython3
   ds.check()


This will carry out a number of checks. First, it will check if there are any variables with integer data types. Second, it will check if the time dimension is stored as an integer data type, which can potentially cause problems. Third, it will check if files are CF-compliant. Lack of CF-compliance could point towards problems with CDO interpreting the contents of the dataset, and thus problems in nctoolkit. Finally, it will check if the variables in a datset have the same horizontal grids.



How to fix a dataset with coordinates as variables
---------------

Sometimes longitude and latitude will be stored as variables in a netCDF file. Ideally they should be coordinates for nctoolkit to work fully.
You can fix this using the ``assign_coords`` method as follows:


.. code:: ipython3
   ds.assign_coords(lon_name = "lon", lat_name = "lat")

where `lon_name` and `lat_name` should be the name of the longitude and latitude variables.




