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
    data = nc.open_data("sst.mon.mean.nc")
    data.tmean()

However, you may want to calculate, for example, an annual average. To
do this we use ``over``. This is a list which tells the function which
time periods to average over. For example, the following will calculate
an annual average:

.. code:: ipython3

    data.tmean(["year"])

If you are only averaging over one time period, as above, you can simply
use a character string:

.. code:: ipython3

    data.tmean("year")

The possible options for ``over`` are “day”, “month”, “year”, and
“season”. In this case “day” stands for day of year, not day of month.

In the example below we are calculating the maximum value in each month
of each year in the dataset.

.. code:: ipython3

    data.tmax(["month", "year"])

Calculating climatologies
-------------------------

This means we can easily calculate climatologies. For example the
following will calculate a seasonal climatology:

.. code:: ipython3

    data.tmean("season")

These methods all partial matches for the arguments, which means you do
not need to remember the precise argument each time. For example, the
following will also calculate a seasonal climatology:

.. code:: ipython3

    data.tmean("Seas")

Calculating a climatological monthly mean would require the following:

.. code:: ipython3

    data.tmean("month")

and daily would be the following:

.. code:: ipython3

    data.tmean("day")

Cumulative sums
---------------

We can calculate the cumulative sum as follows:

.. code:: ipython3

    data.tcumsum()

Please note that this can only calculate over all time periods, and does
not accept an ``over`` argument.
