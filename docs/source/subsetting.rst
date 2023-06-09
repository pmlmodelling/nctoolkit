Subsetting data
===============

nctoolkit has many built in methods for subsetting data. The main method
is ``subset``. This let’s you select specific variables, years, months,
seasons and timesteps.

Selecting variables
-------------------

If you want to select specific variables, you would do the following:

.. code:: ipython3

    ds.subset(variables = ["var1", "var2"])

If you only want to select one variable, you can do this:

.. code:: ipython3

    ds.subset(variables = "var1")

Selecting years
---------------


If you want to select specific years, you can do the following:

.. code:: ipython3

    ds.subset(years = [2000, 2001])

Again, if you want a single year the following will work:

.. code:: ipython3

    ds.subset(years = 2000)

The ``select`` method allows partial matches for its arguments. So if we
want to select the year 2000, the following will work:

.. code:: ipython3

    ds.subset(year = 2000)

In this case we can also select a range. So the following will work:

.. code:: ipython3

    ds.subset(years = range(2000, 2010))

Selecting months
----------------

You can select months in the same way as years. The following examples
will all do the same thing:

.. code:: ipython3

    ds.subset(months = [1,2,3,4])
    ds.subset(months = range(1,5))
    ds.subset(mon = [1,2,3,4])

Selecting seasons
-----------------

You can easily select seasons. For example if you wanted to select
winter, you would do the following:

.. code:: ipython3

    ds.subset(season = "DJF")

Selecting timesteps
-------------------

You can select specific timesteps from a dataset in a similar manner.
For example if you wanted to select the first two timesteps in a dataset
the following two methods will work:

.. code:: ipython3

    ds.subset(time = [0,1])
    ds.subset(time = range(0,2))

Geographic subsetting
---------------------

If you want to select a geographic subregion of a dataset, you can use
`subset`. This method will select all data within a specific
longitude/latitude box. You just need to supply the minimum longitude
and latitude required. In the example below, a dataset is cropped with
longitudes between -80 and 90 and latitudes between 50 and 80:


.. code:: ipython3

    ds.subset(lon = [-80, 90], lat = [50, 80])


