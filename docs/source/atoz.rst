An A-Z guide to nctoolkit methods
=================================

This guide will provide examples of how to use almost every method
available in nctoolkit.

add
---

This method can add to a dataset. You can add a constant, another
dataset or a NetCDF file. In the case of datasets or NetCDF files the
grids etc. must be of the same structure as the original dataset.

For example, if we had a temperature dataset where temperature was in
Celsius, we could convert it to Kelvin by adding 273.15.

.. code:: ipython3

    data = nc.open_data(infile)
    data.add(273.15)

If we have two sets, we add one to the other as follows:

.. code:: ipython3

    data1 = nc.open_data(infile1)
    data2 = nc.open_data(infile2)
    data1.add(data2)

In the above example, all we are doing is adding infile2 to data2, so
instead we could simply do this:

.. code:: ipython3

    data1.add(infile2)

annual_anomaly
--------------

This method will calculate the annual anomaly for each variable (and in
each grid cell) compared with a baseline. This is a standard anomaly
calculation where first the mean value is calculated for the baseline
period, and the difference between the values is calculated.

For example, if we wanted to calculate the anomalies in a dataset
compared with a baseline period of 1900-1919 we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_anomaly(baseline=[1900, 1919])

We may be more interested in the rolling anomaly, in particular when
there is a lot of annual variation. In the above case, if you wanted a
20 year rolling mean anomaly, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_anomaly(baseline=[1900, 1919], window=20)

By default this method works out the absolute anomaly. However, in some
cases the relative anomaly is more interesting. To calculate this we set
the metric argument to “relative”:

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_anomaly(baseline=[1900, 1919], metric = "relative")

annual_max
----------

This method will calculate the maximum value in each available year and
for each grid cell of dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_max()

annual_mean
-----------

This method will calculate the maximum value in each available year and
for each grid cell of dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_mean()

annual_min
----------

This method will calculate the minimum value in each available year and
for each grid cell of dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_min()

annual_range
------------

This method will calculate the range of values in each available year
and for each grid cell of dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_range()

bottom
------

This method will extract the bottom vertical level from a dataset. This
is useful for some oceanographic datasets, where the method can let you
select the seabed. Note that this method will not work with all data
types. For example, in ocean data with fixed depth levels, the bottom
cell in the NetCDF data is not the actual seabed. See bottom_mask for
these cases.

.. code:: ipython3

    data = nc.open_data(infile)
    data.bottom()

bottom_mask
-----------

This method will identify the bottommost level in each grid with a
non-NA value.

.. code:: ipython3

    data = nc.open_data(infile)
    data.bottom_mask()

cdo_command
-----------

This method let’s you run a cdo command. CDO commands are generally of
the form “cdo {command} infile outfile”. cdo_command therefore only
requires the command portion of this. If we wanted to run the following
CDO command

::

   cdo -timmean -selmon,4 infile outfile

we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.cdo_command("-timmean -selmon,4")

cell_areas
----------

This method either adds the areas of each grid cell to the dataset or
converts the dataset to a new dataset showing only the grid cell areas.
By default it adds the cell areas (in square metres) to the dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.cell_areas()

If we only want the cell areas we can set join to False:

.. code:: ipython3

    data.cell_areas(join=False)

clip
----

This method will clip a region to a specified longitude and latitude
box. For example, if we wanted to clip a dataset to the North Atlantic,
we could do this:

.. code:: ipython3

    data = nc.open_data(infile)
    data.clip(lon = [-80, 20], lat = [40, 70])

compare_all
-----------

This method let’s us compare all variables in a dataset with a constant.
If we wanted to identify the grid cells with values above 20, we could
do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.compare_all(">20")

Similarly, if we wanted to identify grid cells with negative values we
would do this:

.. code:: ipython3

    data = nc.open_data(infile)
    data.compare_all("<0")

cor_space
---------

This method calculates the correlation coefficients between two
variables in space for each time step. So, if we wanted to work out the
correlation between the variables var1 and var2, we would do this:

.. code:: ipython3

    data = nc.open_data(infile)
    data.cor_space("var1", "var2")

cor_time
--------

This method calculates the correlation coefficients between two
variables in time for each grid cell. If we wanted to work out the
correlation between two variables var1 and var2 we would do the
following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.cor_time("var1", "var2")

cum_sum
-------

This method will calculate the cumulative sum, over time, for all
variables. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.cum_sum()

daily_max_climatology
---------------------

This method will calculate the maximum value that is observed on each
day of the year over time. So, for example, if you had 100 years of
daily temperature data, it will calculate the maximum value ever
observed on each day.

.. code:: ipython3

    data = nc.open_data(infile)
    data.daily_max_climatology()

daily_mean_climatology
----------------------

This method will calculate the mean value that is observed on each day
of the year over time. So, for example, if you had 100 years of daily
temperature data, it will calculate the mean value ever observed on each
day.

.. code:: ipython3

    data = nc.open_data(infile)
    data.daily_mean_climatology()

daily_min_climatology
---------------------

This method will calculate the minimum value that is observed on each
day of the year over time. So, for example, if you had 100 years of
daily temperature data, it will calculate the minimum value ever
observed on each day.

.. code:: ipython3

    data = nc.open_data(infile)
    data.daily_min_climatology()

daily_range_climatology
-----------------------

This method will calculate the value range that is observed on each day
of the year over time. So, for example, if you had 100 years of daily
temperature data, it will calculate the difference between the maximum
and minimum observed values each day.

.. code:: ipython3

    data = nc.open_data(infile)
    data.daily_range_climatology()

divide
------

This method will divide a dataset by a constant, or the values in
another dataset of NetCDF file. If we wanted to divide everything in a
dataset by 2, we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.divide(2)

If we want to divide a dataset by another, we can do this easily. Note
that the datasets must be comparable, i.e. they must have the same grid.
The second dataset must have either the same number of variables or only
one variable. In the latter case everything is divided by that variable.
The same holds for vertical levels.

.. code:: ipython3

    data1 = nc.open_data(infile1)
    data2 = nc.open_data(infile2)
    data1.divide(data2)

ensemble_max, ensemble_min, ensemble_range and ensemble_mean
------------------------------------------------------------

These methods will calculate the ensemble statistic, when a dataset is
made up of multiple files. Two methods are available. First, the
statistic across all available time steps can be calculated. For this
ignore_time must be set to False. For example:

.. code:: ipython3

    data = nc.open_data(file_list)
    data.ensemble_max(ignore_time = True)

The second method is to calculate the maximum value in each given time
step. For example, if the ensemble was made up of 100 files where each
file contains 12 months of data, ensemble_max will work out the maximum
monthly value. By default ignore_time is False.

.. code:: ipython3

    data = nc.open_data(file_list)
    data.ensemble_max(ignore_time = False)

ensemble_percentile
-------------------

This method works in the same way as ensemble_mean etc. above. However,
it requires an additional term p, which is the percentile. For example,
if we had to calculate the 75th ensemble percentile, we would do the
following:

.. code:: ipython3

    data = nc.open_data(file_list)
    data = nc.ensemble_percentile(75)

invert_levels
-------------

This method will invert the vertical levels of a dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.invert_levels()

mask_box
--------

This method will set everything outside a specificied longitude/latitude
box to NA. The code below illustrates how to mask the North Atlantic in
the SST dataset.

.. code:: ipython3

    data = nc.open_data(infile)
    data.mask_box(lon = [-80, 20], lat = [40, 70])

max
---

This method will calculate the maximum value of all variables in all
grid cells. If we wanted to calculate the maximum observed monthly sea
surface temperature in the SST dataset we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.max()

mean
----

This method will calculate the mean value of all variables in all grid
cells. If we wanted to calculate the maximum observed monthly sea
surface temperature in the SST dataset we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.mean()

merge and merge_time
--------------------

nctoolkit offers two methods for merging the files within a multi-file
dataset. These methods operate in a similar way to column based joining
and row-based binding in dataframes.

The merge method is suitable for merging files that have different
variables, but the same time steps. The merge_time method is suitable
for merging files that have the same variables, but have different time
steps.

Usage for merge_time is as simple as:

.. code:: ipython3

    data = nc.open_data(file_list)
    data.merge_time()

Merging NetCDF files with different variables is potentially risky, as
it is possible you can merge files that have the same number of time
steps but have different times. nctoolkit’s merge method therefore
offers some security against a major error when merging. It requires a
match argument to be supplied. This ensures that the times in each file
is comparable to the others. By default match = [“year”, “month”,
“day”], i.e. it checks if the times in each file all have the same year,
month and day. The match argument must be some subset of [“year”,
“month”, “day”]. For example, if you wanted to only make sure the files
had the same year, you would do the following:

.. code:: ipython3

    data = nc.open_data(file_list)
    data.merge(match = ["year", "month", "day"])

max
---

This method will calculate the maximum value of all variables in all
grid cells. If we wanted to calculate the maximum observed monthly sea
surface temperature in the SST dataset we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.max()

mean
----

This method will calculate the mean value of all variables in all grid
cells. If we wanted to calculate the mean observed monthly sea surface
temperature in the SST dataset we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.mean()

monthly_anomaly
---------------

This method will calculate the monthly anomaly compared with the mean
value for a baseline period. For example, if we wanted the monthly
anomaly compared with the mean for 1990-1999 we would do the below.

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_anomaly(baseline = [1990, 1999])

monthly_max
-----------

This method will calculate the maximum value in the month of each year
of a dataset. This is useful for daily time series. If you want to
calculate the mean value in each month across all available years, use
monthly_max_climatology. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_max()

monthly_max_climatology
-----------------------

.. code:: ipython3

    This method will calculate, for each month, the maximum value of each variable over all time steps.

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_max_climatology()

monthly_mean
------------

This method will calculate the mean value of each variable in each month
of a dataset. Note that this is calculated for each year. See
monthly_mean_climatology if you want to calculate a climatological
monthly mean.

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_mean()

monthly_mean_climatology
------------------------

This method will calculate, for each month, the maximum value of each
variable over all time steps. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_mean_climatology()

monthly_min
-----------

This method will calculate the minimum value in the month of each year
of a dataset. This is useful for daily time series. If you want to
calculate the mean value in each month across all available years, use
monthly_max_climatology. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_min()

monthly_min_climatology
-----------------------

This method will calculate, for each month, the minimum value of each
variable over all time steps. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_min_climatology()

monthly_range
-------------

This method will calculate the value range in the month of each year of
a dataset. This is useful for daily time series. If you want to
calculate the value range in each month across all available years, use
monthly_range_climatology. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_range()

monthly_range_climatology
-------------------------

This method will calculate, for each month, the value range of each
variable over all time steps. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.monthly_range_climatology()

multiply
--------

This method will multiply a dataset by a constant, another dataset or a
NetCDF file. If multiplied by a dataset or NetCDF file, the dataset must
have the same grid and can only have one variable.

If you want to multiply a dataset by 2, you can do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.multiply(2)

If you wanted to multiply a dataset data1 by another, data2, you can do
the following:

.. code:: ipython3

    data1 = nc.open_data(infile1)
    data2 = nc.open_data(infile2)
    data1.multiply(data2)

mutate
------

This method can be used to generate new variables using arithmetic
expressions. New variables are added to the dataset. The method requires
a dictionary, where the key-value pairs are the new variables and
expression required to generate it.

For example, if had a temperature dataset, with temperature in Celsius,
we might want to convert that to Kelvin. We can do this easily:

.. code:: ipython3

    data = nc.open_data(infile)
    data.mutate({"temperature_k":"temperature+273.15"})

percentile
----------

This method will calculate a given percentile for each variable and grid
cell. This will calculate the percentile using all available timesteps.

We can calculate the 75th percentile of sea surface temperature as
follows:

.. code:: ipython3

    data = nc.open_data(infile)
    data.percentile(75)

phenology
---------

A number of phenological indices can be calculated. These are based on
the plankton metrics listed by `Ji et
al. 2010 <https://academic.oup.com/plankt/article/32/10/1355/1438955>`__.
These methods require datasets or the files within a dataset to only be
made up of individual years, and ideally every day of year is available.
At present this method can only calculate the phenology metric for a
single variable.

The available metrics are: peak - the time of year when the maximum
value of a variable occurs. middle - the time of year when 50% of the
annual cumulative sum of a variable is first exceeded start - the time
of year when a lower threshold (which must be defined) of the annual
cumulative sum of a variable is first exceeded end - the time of year
when an upper threshold (which must be defined) of the annual cumulative
sum of a variable is first exceeded

For example, if you wanted to calculate timing of the peak, you set
metric to “peak”, and define the variable to be analyzed:

.. code:: ipython3

    data = nc.open_data(infile)
    data.phenology(metric = "peak", var = "var_chosen")

plot
----

This method will plot the contents of a dataset. It will either show a
map or a time series, depending on the data type. While it should work
on at least 90% of NetCDF data, there are some data types that remain
incompatible, but will be added to nctoolkit over time. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.plot()

range
-----

This method calculates the range for all variables in each grid cell
across all steps.

We can calculate the range of sea surface temperatures in the SST
dataset as follows:

.. code:: ipython3

    data = nc.open_data(infile)
    data.range()

regrid
------

This method will remap a dataset to a new grid. This grid must be either
a pandas data frame, a NetCDF file or a single file nctoolkit dataset.

For example, if we wanted to regrid a dataset to a single location, we
could do the following:

.. code:: ipython3

    import pandas as pd
    data = nc.open_data(infile)
    grid = pd.DataFrame({"lon":[-20], "lat":[50]})
    data.regrid(grid, method = "nn")

If we wanted to regrid one dataset, dataset1, to the grid of another,
dataset2, using bilinear interpolation, we would do the following:

.. code:: ipython3

    data1 = nc.open_data(infile1)
    data2 = nc.open_data(infile2)
    data1.regrid(data2, method = "bil")

remove_variables
----------------

This method will remove variables from a dataset. Usage is simple, with
the method only requiring either a str of a single variable or a list of
variables to remove:

.. code:: ipython3

    data = nc.open_data(infile)
    data.remove_variables(vars)

rename
------

This method allows you to rename variables. It requires a dictionary,
with key-value pairs representing the old variable names and new
variables. For example, if we wanted to rename a variable old to new, we
would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rename({"old":"new"})

rolling_max
-----------

This method will calculate the rolling maximum over a specifified
window. For example, if you needed to calculate the rolling maximum with
a window of 10, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rolling_max(window = 10)

rolling_mean
------------

This method will calculate the rolling mean over a specifified window.
For example, if you needed to calculate the rolling mean with a window
of 10, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rolling_mean(window = 10)

rolling_min
-----------

This method will calculate the rolling minimum over a specifified
window. For example, if you needed to calculate the rolling minimum with
a window of 10, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rolling_min(window = 10)

rolling_range
-------------

This method will calculate the rolling range over a specifified window.
For example, if you needed to calculate the rolling range with a window
of 10, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rolling_range(window = 10)

rolling_sum
-----------

This method will calculate the rolling sum over a specifified window.
For example, if you needed to calculate the rolling sum with a window of
10, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.rolling_sum(window = 10)

run
---

This method will evaluate all of a dataset’s unevaluated commands. Usage
is simple:

.. code:: ipython3

    nc.options(lazy = True)
    data = nc.open_data(infile)
    data.select_years(1990)
    data.run()

seasonal_max
------------

This method will calculate the maximum value observed in each season.
Note this is worked out for the seasons of each year. See
seasonal_max_climatology for climatological seasonal maximums.

.. code:: ipython3

    data.seasonal_max()

seasonal_max_climatology
------------------------

This method calculates the maximum value observed in each season across
all years. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_max_climatology()

seasonal_mean
-------------

This method will calculate the mean value observed in each season. Note
this is worked out for the seasons of each year. See
seasonal_mean_climatology for climatological seasonal means.

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_mean()

seasonal_mean_climatology
-------------------------

This method calculates the mean value observed in each season across all
years. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_mean_climatology()

seasonal_min
------------

This method will calculate the minimum value observed in each season.
Note this is worked out for the seasons of each year. See
seasonal_min_climatology for climatological seasonal minimums.

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_min()

seasonal_min_climatology
------------------------

This method calculates the minimum value observed in each season across
all years. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_min_climatology()

seasonal_range
--------------

This method will calculate the value range observed in each season. Note
this is worked out for the seasons of each year. See
seasonal_range_climatology for climatological seasonal ranges.

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_range()

seasonal_range_climatology
--------------------------

This method calculates the value range observed in each season across
all years. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.seasonal_range_climatology()

select_months
-------------

This method allows you to subset a dataset to specific months. This can
either be a single month, a list of months or a range. For example, if
we wanted the first half of a year, we would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.select_months(range(1, 7))

select_variables
----------------

This method allows you to subset a dataset to specific variables. This
either accepts a single variable or a list of variables. For example, if
you wanted two variables, var1 and var2, you would do the following:

.. code:: ipython3

    data = nc.open(infile)
    data.select_variables(["var1", "var2"])

select_years
------------

This method subsets datasets to specified years. It will accept either a
single year, a list of years, or a range. For example, if you wanted to
subset a dataset the 1990s, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.select_years(range(1990, 2000))

set_missing
-----------

This method allows you to set a range to missing values. It either
accepts a single variable or two variables, specifying the range to be
set to missing values. For example, if you wanted all values between 0
and 10 to be set to missing, you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.set_missing([0, 10])


shift_days
-----------

This method allows you to move the times in a dataset forwards or backwards by a number of days. It takes one argument: the number of days to shift by. For example, if you wanted to shift time back 2 days, you would do the following:

.. code:: ipython3

    data.shift_days(-2)

shift_hours
-----------

This method allows you to move the times in a dataset forwards or backwards by a number of hours. It takes one argument: the number of hours to shift by. For example, if you wanted to shift time back 6 hours, you would do the following:

.. code:: ipython3

    data.shift_hours(-6)



spatial_max
-----------

This method will calculate the maximum value observed in space for each
variable and time step. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_max()

spatial_mean
------------

This method will calculate the spatial mean for each variable and time
step. If the grid cell area can be calculated, this will be an area
weighted mean. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_mean()

spatial_min
-----------

This method will calculate the minimum observed in space for each
variable and time step. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_min()

spatial_percentile
------------------

This method will calculate the percentile of variable across space for
time step. For example, if you wanted to calculate the 75th percentile,
you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_percentile(p=75)

spatial_range
-------------

This method will calculate the value range observed in space for each
variable and time step. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_range()

spatial_sum
-----------

This method will calculate the spatial sum for each variable and time
step. In some cases, for example when variables are concentrations, it
makes more sense to multiply the value in each grid cell by the grid
cell area, when doing a spatial sum. This method therefore has an
argument by_area which defines whether to multiply the variable value by
the area when doing the sum. By default by_area is False.

Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.spatial_sum()

split
-----

Except for methods that begin with merge or ensemble, all nctoolkit
methods operate on individual files within a dataset. There are
therefore cases when you might want to be able to split a dataset into
separate files for analysis. This can be done using split, which let’s
you split a file into separate years, months or year/month combinations.
For example, if you want to split a dataset into files of different
years, you can do this:

.. code:: ipython3

    data = nc.open_data(infile)
    data.split("year")

subtract
--------

This method can subtract from a dataset. You can substract a constant,
another dataset or a NetCDF file. In the case of datasets or NetCDF
files the grids etc. must be of the same structure as the original
dataset.

For example, if we had a temperature dataset where temperature was in
Kelvin, we could convert it to Celsiu by subtracting 273.15.

.. code:: ipython3

    data = nc.open_data(infile)
    data.substract(273.15)

sum
---

This method will calculate the sum of values of all variables in all
grid cells. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.sum()

surface
-------

This method will extract the surface level from a multi-level dataset.
Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.surface()

to_dataframe
------------

This method will return a pandas dataframe with the contents of the
dataset. This has a decode_times argument to specify whether you want
the times to be decoded. Defaults to True. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.to_dataframe()

to_latlon
---------

This method will regrid a dataset to a regular latlon grid. The minimum
and maximum longitudes and latitudes must be specified, along with the
horizontal and vertical resolutions.

.. code:: ipython3

    data = nc.open_data(infile)
    data.to_latlon(lon = [-80, 20], lat = [30, 80], res = [1,1])

to_xarray
---------

This method will return an xarray datasetwith the contents of the
dataset. This has a decode_times argument to specify whether you want
the times to be decoded. Defaults to True. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.to_xarray()

transmute
---------

This method can be used to generate new variables using arithmetic
expressions. Existing will be removed from the dataset. See mutate if
you want to keep existing variables. The method requires a dictionary,
where the key-value pairs are the new variables and expression required
to generate it.

For example, if had a temperature dataset, with temperature in Celsius,
we might want to convert that to Kelvin. We can do this easily:

.. code:: ipython3

    data = nc.open_data(infile)
    data.transmute({"temperature_k":"temperature+273.15"})

var
---

This method calculates the variance of each variable in the dataset.
This is calculate across all time steps. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.var()

vertical_interp
---------------

This method interpolates variables vertically. It requires a list of
vertical levels, for example depths, you want to interpolate. For
example, if you had an ocean dataset and you wanted to interpolate to 10
and 20 metres you would do the following:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_interp(levels = [10, 20])

vertical_max
------------

This method calculates the maximum value of each variable across all
vertical levels. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_max()

vertical_mean
-------------

This method calculates the mean value of each variable across all
vertical levels. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_mean()

vertical_min
------------

This method calculates the minimum value of each variable across all
vertical levels. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_min()

vertical_range
--------------

This method calculates the value range of each variable across all
vertical levels. Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_range()

vertical_sum
------------

This method calculates the sum each variable across all vertical levels.
Usage is simple:

.. code:: ipython3

    data = nc.open_data(infile)
    data.vertical_sum()

write_nc
--------

This method allows you to write the contents of a dataset to a NetCDF
file. If the target file exists and you want to overwrite it set
overwrite to True. Usage is simple:

.. code:: ipython3

    data.write_nc(outfile)

zip
---

This method will zip the contents of a dataset. This is mostly useful
for processing chains where you want to minimize disk space usage by the
output. Please note this method works lazily. In the code below only one
file is generated, a zipped “outfile”.

.. code:: ipython3

    nc.options(lazy = True)
    data = nc.open_data(infile)
    data.select_years(1990)
    data.zip()
    data.write_nc(outfile)

Zonal statistics
----------------

If you want to calculate zonal statistics, a number of methods are
available: zonal_mean, zonal_min, zonal_max and zonal_range. Usage is
simple. For example to calculate the zonal mean you would do the
following:

.. code:: ipython3

    data.zonal_mean()
