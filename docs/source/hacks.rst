Random Data Hacks
------------------

nctoolkit features a number of useful methods to tweak data.


Shifting time
================

Sometimes the times in datasets are not quite what we want, and we need some way to adjust time. An example of this
is when you are missing a year of data, so want to copy data from the prior year and use it. But first you would need
to shift the times in that year forward by a year. You can do this with the ``shift`` method. This let's you shift
time forward by a specified number of hours, days, months or years. You just need to supply hours, days, months or years
as an argument. So, if you wanted to shift time backward by one year, you would do the following:

.. code:: ipython3

    ds.shift(years = -1)

If you wanted to shift time forward by 12 hours, this would do it:


.. code:: ipython3

    ds.shift(hours = 12)

Note: this method allows partial matches to the arguments, so you could use hour, day, month or year just as easily. 


Adding cell areas to a dataset
================

You can add grid cell areas to a dataset as follows:

.. code:: ipython3

    ds.cell_area()

By default, this will add the cell area (in square metres) to the dataset. If you want the dataset to only include cell areas
you need to set the ``join`` argument to ``False``:


.. code:: ipython3

    ds.cell_area(join = False)

Of course, this method will only if it is possible to calculate the areas the grid cells.


Changing the format of the netCDF files in a dataset
================

Sometimes you will want to change the format of the files in a dataset. You can do this using the ``format`` method. This let's
you set the format, with the following options: 
  * netCDF = "nc1"
  * netCDF version 2 (64-bit offset) = "nc2"/"nc"
  * netCDF4 (HDF5) = "nc4"
  * netCDF4-classi = "nc4c"
  * netCDF version 5 (64-bit data) = "nc5"


So, if you want to set the format to netCDF4, you would do the following:

.. code:: ipython3

    ds.format("nc4")



Getting rid of dimensions with only one value
================

Sometimes you will have a dataset that has a dimension with only one value, and you might want to get rid of that dimension. For example,
you might only have one one timestep and keeping it may have no value. Getting rid of that dimension can be done using the ``reduce_dims`` method. 
It works as follows:

.. code:: ipython3

    ds.reduce_dims() 




