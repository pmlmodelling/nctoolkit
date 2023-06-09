Introduction to nctoolkit
============


nctoolkit is a multi-purpose tool for analyzing and post-processing netCDF files. 
It is designed explicitly with climate change and oceanographic work in mind. Under the hood, it uses `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/>`__ (CDO), but it operates as a stand-alone package with no knowledge of CDO being required to use it.



Let's look at what it can do using a historical global dataset of sea surface temperature, which you can find `here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.


The preferred way to import nctoolkit is:

.. code:: python3

   import nctoolkit as nc

   
It lets you quickly visualize data
----------------------------------

nctoolkit offers plotting functionality that will let you automatically plot data from almost any type of netCDF file. It's as simple as the following, which calculates mean historical sea surface temperature and then plots it:

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.subset(year = 2000)
   ds.plot()


.. raw:: html
   :file: intro_plot1.html 

It lets you easily subset data
---------------------

If we want to look at a particular region, we can subset the data using the 'subset' method, and further select a particular year and month, we can do this as follows:


.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.subset(year = 1998, month = 1, lon = [-13, 38], lat = [30, 67])
   ds.plot()


.. raw:: html
   :file: intro_plot4.html

It lets you calculate temporal averages
---------------------------------------

nctoolkit features a suite of methods, beginning with the letter t, that let you calculate temporal statistics. For example, if we wanted to calculate how much sea surface temperature varies each year, we could do this:

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.tmean()
   ds.plot()

.. raw:: html
   :file: intro_plot6.html


It lets you calculate spatial averages
--------------------------------------

Calculating the spatial average of a variable is as simple as:

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.spatial_mean()
   ds.plot()

.. raw:: html
   :file: intro_plot2.html

It lets you do mathematical operations
--------------------------------------

nctoolkit offers an 'assign' method for performing mathematical operations on variables. This works in a way that will be familiar to users of Pandas. The method is illustrated below in a processing chain that works out how much warmer each part of the ocean is than the global mean. 

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.tmean()
   ds.assign(delta = lambda x: x.sst - spatial_mean(x.sst), drop = True)
   ds.plot("anomaly")

.. raw:: html
   :file: intro_plot3.html


It lets you regrid data
-----------------------

nctoolkit has built-in methods for regridding data to user-specified grids. One of the most useful is `to_latlon`. This let's you regrid to a regular latlon grid. You just need to specify the extent of the new grid, the resolution and the regridding method.

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.subset(time = 0)
   ds.to_latlon(lon = [-13, 38], lat = [30, 67], resolution = 1, method = "bilinear")
   ds.plot()

.. raw:: html
   :file: intro_plot5.html


It lets you calculate anomalies
---------------------------------------

In an example above we calculated the global mean sea surface temperature every month since 1850. But calculate the anomaly might be more interesting. The code below will calculate the change in  global annual mean sea surface temperature since 1850-1969. The window argument let's you calculate it on a rolling basis.


.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.spatial_mean()
   ds.annual_anomaly(baseline = [1850, 1869], window= 20)
   ds.plot()

.. raw:: html
   :file: intro_plot7.html

It lets you calculate zonal averages
---------------------------------------

It is easy to calculate zonal averages using nctoolkit. In the example below change in temperature since 1850-1869 in each latitude band is calculated:

.. code:: ipython3

   ds = nc.open_data("sst.mon.mean.nc")
   ds.annual_anomaly(baseline = [1850, 1869], window= 20)
   ds.zonal_mean()
   ds.plot()

.. raw:: html
   :file: intro_plot8.html

