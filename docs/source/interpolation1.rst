Interpolation
============

nctoolkit features built in methods for horizontal and vertical interpolation.

Horizontal interpolation
-------------------------

We will illustrate how to carry out horizontal interpolation using a global dataset of global SST from NOAA. Find out more information about the datset `here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.


The data is available using a thredds server. So we will work with the first time step, which looks like this:


.. code:: ipython3


   import nctoolkit as nc
   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(time = 0)
   ds.plot()

.. raw:: html
   :file: interpolation_plot1.html 


Interpolating to a set of coordinates
--------------------------------------


If you want to regrid a dataset to a specified set of coordinates you
can ``regrid`` and a pandas dataframe. The first column of the dataframe
should be the longitudes and the second should be latitudes. The example
below regrids a sea-surface temperature dataset to a single location
with longitude -30 and latitude 50.


.. code:: ipython3

   import pandas as pd
   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0) 
   coords = pd.DataFrame({"lon":[-30], "lat":[50]})
   ds.regrid(coords)
   ds.to_dataframe()


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>lon</th>
          <th>lat</th>
          <th>sst</th>
        </tr>
        <tr>
          <th>time</th>
          <th>ncells</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1850-01-01</th>
          <th>0</th>
          <td>-30.0</td>
          <td>50.0</td>
          <td>10.935501</td>
        </tr>
      </tbody>
    </table>
    </div>


Interpolating to a regular lonlat grid
---------------------------------------

If you want to interpolate to a regular latlon grid, you can use ``to_latlon``. ``lon`` and ``lat`` specify the minimum and maximum longitudes and latitudes, while ``res``, a 3 variable list specifies the resolution. For example, if we wanted to regrid the globe to 0.5 degree north-south by 1 degree east-west resolution, we could do the following:


.. code:: ipython3


   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0)
   ds.to_latlon(lon = [-79.5, 79.5], lat = [0.75, 89.75], res = [1, 0.5])
   ds.plot()

.. raw:: html
   :file: interpolation_plot2.html


Interpolating to another dataset’s grid
---------------------------------------
If we are working with two datasets and want to put them on a common grid, we can interpolate one onto the other’s grid. We can illustate this with a dataset of global sea surface temperature. Let’s start by cropping this dataset to the northern hemisphere. 


.. code:: ipython3
   ds1 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds1.subset(timestep = 0)
   ds1.subset(lat = [0, 90]) 
   ds1.plot()

.. raw:: html
   :file: interpolation_plot3.html


Now, we can regrid the original file to this northern hemisphere grid.

.. code:: ipython3
   ds2 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds2.subset(timestep = 0)
   ds2.regrid(ds1)
   ds2.plot()


.. raw:: html
   :file: interpolation_plot4.html

This method will also work using netCDF files. So, if you wanted you can also use a path to a netCDF file as the target grid.


How to reuse the weights for regridding
---------------------------------------
Under the hood nctoolkit regrids data by first generating a weights file. There are situations where you  will want to be able to re-use these weights. For example, if you are post-processing a large number of files one after the other. To make this easier nctoolkit let's you recycle the regridding info. This let's you interpolate using either ``regrid`` or ``to_latlon``, but keep the regridding data for future use by ``regrid``.



.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0)
   ds.to_latlon(lon = [-79.5, 79.5], lat = [-0.75, 89.75], res = [1, 0.5], recycle = True)
   ds.plot()
.. raw:: html
   :file: interpolation_plot5.html


.. code:: ipython3
   ds1 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds1.subset(timestep = 0)
   ds1.regrid(ds)
   ds1.plot()

.. raw:: html
   :file: interpolation_plot6.html

Horizontal Resampling
---------------------

If you want to make data more coarse spatially, just use the ``resample_grid`` method. This will, for example, let you select every 2nd grid grid cell in a north-south and east-west direction. This is illustrated in the example below, where a dataset which has spatial resolution of 1 by 1 degrees is coarsened, so that only every 10th cell is selected in a north-south and east-west. In other words it is now a 10 degrees by 10 degrees dataset.


.. code:: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0)
   ds.resample_grid(10)
   ds.plot()

.. raw:: html
   :file: interpolation_plot7.html

spatial infilling
-----------------

Some times you will have data with missing values, which you want to replace with a nearby value. nctoolkit handles this situation using the ``fill_na`` method. This uses distance-weighting. You just need to specify the number of nearest-neighbours to use for the weighting. For example, if you simply want to replace missing values with their nearest neighbour, you just set the number to 1, as follows:

..code :: ipython3

   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0)
   ds.fill_na(1)
   ds.plot()

..raw:: html
   :file: interpolation_plot8.html

## Vertical interpolation

We can carry out vertical interpolation using the ``vertical_interp`` method. This is particularly useful for oceanic data. This is illustrated below by interpolating depth-resolved ocean temperatures from `NOAA’s World Ocean Atlas <https://www.ncei.noaa.gov/products/world-ocean-atlas>`__ for January to a depth of 500 metres. The ``vertical_interp`` method requires a ``levels`` argument, which is sea-depth in this case. 

..code :: ipython3

   ds = nc.open_thredds("https://www.ncei.noaa.gov/thredds/dodsC/ncei/woa/temperature/decav/1.00/woa18_decav_t00_01.nc")
   ds.subset(timestep = 0)
   ds.vertical_interp(levels = 500, fixed = True)
   ds.plot()

..raw:: html
   :file: interpolation_plot9.html







