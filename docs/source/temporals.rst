Temporal statistics
===================

nctoolkit has a number of built-in methods for calculating temporal
statistics, all of which are prefixed with t: ``tmean``, ``tmin``,
``tmax``, ``trange``, ``tpercentile``, ``tmedian``, ``tvariance``,
``tstdev`` and ``tcumsum``.

These methods allow you to quickly calculate temporal statistics over
specified time periods using the ``over`` argument.

By default the methods calculate the value over all time steps
available. For example the following will calculate the temporal mean:

.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_data("sst.mon.mean.nc")
    ds.tmean()

However, you may want to calculate, for example, an annual average. To
do this we use ``over``. This is a list which tells the function which
time periods to average over. For example, the following will calculate
an annual average:

.. code:: ipython3

    ds.tmean(["year"])

If you are only averaging over one time period, as above, you can simply
use a character string:

.. code:: ipython3

    ds.tmean("year")

The possible options for ``over`` are “day”, “month”, “year”, and
“season”. In this case “day” stands for day of year, not day of month.

In the example below we are calculating the maximum value in each month
of each year in the dataset.

.. code:: ipython3

    ds.tmax(["month", "year"])

Calculating rolling averages
-------------------------

nctoolkit has a range of methods to calcate rolling averages: ``rolling_mean``, ``rolling_min``, ``rolling_max``, ``rolling_range`` and ``rolling_sum``. These
methods let you calculate rolling statistics over a specified time window. For example, if you had daily data and you wanted to calculate a rolling weekly mean
value, you could do the following:



.. code:: ipython3

    ds.rolling_mean(7)


If you wanted to calculated a rolling weekly sum, this would do:

.. code:: ipython3

    ds.rolling_sum(7)

Calculating anomalies 
-------------------------

nctoolkit has two methods for calculating anomalies: ``annual_anomaly`` and ``monthly_anomaly``. Both methods require you to specify a baseline period
to calculate the anomaly against. They require that you specify a baseline period showing the minimum and maximum years of the climatological period to
compare against.

So, if you wanted to calculate the annual anomaly compared with a baseline period of 1950-1969, you would do this:


.. code:: ipython3

    ds.annual_anomaly(baseline = [1950, 1969])

By default, the annual anomaly is calculated as the absolute difference between the annual mean in a year and the mean across the baseline period. However,
in some cases this is not suitable. Instead you might want the relative change. In that case, you would do the following:


.. code:: ipython3

    ds.annual_anomaly(baseline = [1950, 1969], metric = "relative")


You can also smooth out the anomalies, so that they are calculated on a rolling basis. The following will calculate the anomaly using a rolling window of 10
years.

.. code:: ipython3

    ds.annual_anomaly(baseline = [1950, 1969], window = 10) 

Monthly anomalies are calculated in the same way:


.. code:: ipython3

    ds.monthly_anomaly(baseline = [1950, 1969] 

Here the anomaly is the difference between the value in each month compared with the mean in that month during the baseline period.


Calculating climatologies
-------------------------

This means we can easily calculate climatologies. For example the
following will calculate a seasonal climatology:

.. code:: ipython3

    ds.tmean("season")

These methods allow partial matches for the arguments, which means you do
not need to remember the precise argument each time. For example, the
following will also calculate a seasonal climatology:

.. code:: ipython3

    ds.tmean("Seas")

Calculating a climatological monthly mean would require the following:

.. code:: ipython3

    ds.tmean("month")

and daily would be the following:

.. code:: ipython3

    ds.tmean("day")


Calculating climatologies
-------------------------

This means we can easily calculate climatologies. For example the
following will calculate a seasonal climatology:

.. code:: ipython3

    ds.tmean("season")


Cumulative sums
---------------

We can calculate the cumulative sum as follows:

.. code:: ipython3

    ds.tcumsum()

Please note that this can only calculate over all time periods, and does
not accept an ``over`` argument.
