Plotting
--------

nctoolkit provides automatic plotting of netCDF data in a similar way to
the command line tool ncview.

If you have a dataset, simply use the ``plot`` method to create an
interactive plot that matches the data type.

We can illustate this using a sea surface temperature dataset available
`here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.

Let’s start by calculating mean sea surface temperature for the year
2000 and plotting it:

.. code:: ipython3

    import nctoolkit as nc
    ff =  "sst.mon.mean.nc"
    ds = nc.open_data(ff)
    ds.subset(year = 2000)
    ds.plot()

.. raw:: html
   :file: visualization_plot1.html 

.. parsed-literal::

    nctoolkit is using Climate Data Operators version 1.9.10








We might be interested in the zonal mean. nctoolkit can automatically
plot this easily:

.. code:: ipython3

    ff =  "sst.mon.mean.nc"
    ds = nc.open_data(ff)
    ds.subset(year = 2000)
    ds.tmean()
    ds.zonal_mean()
    ds.plot()
