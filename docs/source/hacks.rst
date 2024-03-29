Random Data Hacks
------------------

nctoolkit features a number of useful methods to tweak data.

Handling missing values
================

If you need to set or change missing values, you can use nctoolkit's built-in methods: ``as_missing``, ``missing_as`` and ``set_fill``.

Changing an individual value or values within a range to missing values, is easy using ``as_missing``. If you wanted to set zeroes to missing values, you would do the following:


.. code:: ipython3

    ds.as_missing(0)

In some cases, you might want to set values within a range to missing. In that case, just supply a list to ``as_missing``. The following would set all values from -100 to 0 to missing:

.. code:: ipython3

    ds.as_missing([-1000, 0])


If you need to change missing values to a constant value, use ``missing_as``. The following would change missing values to a constant value of -9999.99:

.. code:: ipython3

    ds.missing_as(-9999.99)

Sometimes you might want to change the fill value used in the netCDF file. This can be particularly useful if you are working with muiltiple files with different fill values. You can do this using using ``set_fill``:

.. code:: ipython3

    ds.set_fill(-9e38)





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



Removing leap days
================

If you want to remove a leap day from a dataset, just do the following:

.. code:: ipython3

    ds.drop(month = 2, day = 29) 



Renaming variables
================

If you want to rename variables, you can use the `rename` method. Just provide a dictionary where the keys are the original
variable names and the values are the new names. So if you wanted to rename a variable x to y, you would do this:

.. code:: ipython3

    ds.rename({"x":"y"})
