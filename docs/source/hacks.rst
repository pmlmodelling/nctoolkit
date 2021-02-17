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

    data.shift(years = -1)

If you wanted to shift time forward by 12 hours, this would do it:


.. code:: ipython3

    data.shift(hours = 12)

Note: this method allows partial matches to the arguments, so you could use hour, day, month or year just as easily. 


Adding cell areas to a dataset
================

You can add grid cell areas to a dataset as follows:

.. code:: ipython3

    data.cell_area()

By default, this will add the cell area (in square metres) to the dataset. If you want the dataset to only include cell areas
you need to set the ``join`` argument to ``False``:


.. code:: ipython3

    data.cell_area(join = False)

Of course, this method will only if it is possible to calculate the areas the grid cells.


Changing the format of the NetCDF files in a dataset
================

Sometimes you will want to change the format of the files in a dataset. You can do this using the ``format`` method. This let's
you set the format, with the following options: 
  * NetCDF = "nc1"
  * NetCDF version 2 (64-bit offset) = "nc2"/"nc"
  * NetCDF4 (HDF5) = "nc4"
  * NetCDF4-classi = "nc4c"
  * NetCDF version 5 (64-bit data) = "nc5"


So, if you want to set the format to NetCDF4, you would do the following:

.. code:: ipython3

    data.format("nc4")

