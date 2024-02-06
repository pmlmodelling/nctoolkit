Introduction to nctoolkit
============


nctoolkit is a multi-purpose tool for analyzing and post-processing netCDF files. 
It is designed explicitly with climate change and oceanographic work in mind. Under the hood, it uses `Climate Data Operators <https://code.mpimet.mpg.de/projects/cdo/>`__ (CDO), but it operates as a stand-alone package with no knowledge of CDO being required to use it.



Let's look at what it can do using a historical global dataset of sea surface temperature, which you learn about `here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.

Here we will use monthly average temperature for the years 1991-2020 and extract data using a thredds server.


The preferred way to import nctoolkit is:

.. code:: python3

   import nctoolkit as nc

   
It lets you quickly visualize data
----------------------------------

nctoolkit offers plotting functionality that will let you automatically plot data from almost any type of netCDF file. It's as simple as the following, which calculates mean historical sea surface temperature and then plots it:

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.plot()


.. raw:: html
   :file: intro_plot1.html 

It lets you easily subset data
---------------------

If we want to look at a particular region, we can subset the data using the 'subset' method, and further select a particular year and month, we can do this as follows:


.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.subset(month = 1, lon = [-13, 38], lat = [30, 67])
   ds.plot()


.. raw:: html
   :file: intro_plot4.html

It lets you calculate temporal averages
---------------------------------------

nctoolkit features a suite of methods, beginning with the letter t, that let you calculate temporal statistics. For example, if we wanted to calculate a seasonal average, we could do this:

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.tmean("season")
   ds.plot()

.. raw:: html
   :file: intro_plot6.html


It lets you calculate spatial averages
--------------------------------------

Calculating the spatial average of a variable is as simple as:

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.subset(variables = "sst")
   ds.subset(lon = [-13, 38], lat = [30, 67])
   ds.spatial_mean()
   ds.plot()

.. raw:: html
   :file: intro_plot2.html

It lets you do mathematical operations
--------------------------------------

nctoolkit offers an 'assign' method for performing mathematical operations on variables. This works in a way that will be familiar to users of Pandas. The method is illustrated below in a processing chain that works out how much warmer each part of the ocean is than the global mean. 

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.tmean()
   ds.assign(delta = lambda x: x.sst - spatial_mean(x.sst), drop = True)
   ds.plot()

.. raw:: html
   :file: intro_plot3.html


It lets you regrid data
-----------------------

nctoolkit has built-in methods for regridding data to user-specified grids. One of the most useful is `to_latlon`. This let's you regrid to a regular latlon grid. You just need to specify the extent of the new grid, the resolution and the regridding method.

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.to_latlon(lon = [-13, 38], lat = [30, 67], res = 1, method = "bil")
   ds.plot()

.. raw:: html
   :file: intro_plot5.html



It lets you calculate zonal averages
---------------------------------------

It is easy to calculate zonal averages using nctoolkit using the `zonal_mean` method. 

.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1991-2020.nc")
   ds.zonal_mean()
   ds.plot()

.. raw:: html
   :file: intro_plot8.html

