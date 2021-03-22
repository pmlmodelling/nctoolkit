Interpolation
=============

nctoolkit features built in methods for horizontal and vertical
interpolation.

Interpolating to a set of coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to regrid a dataset to a specified set of coordinates you
can ``regrid`` and a pandas dataframe. The first column of the dataframe
should be the longitudes and the second should be latitudes. The example
below regrids a sea-surface temperature dataset to a single location
with longitude -30 and latitude 50.

.. code:: ipython3

    import nctoolkit as nc
    import pandas as pd
    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds.select(timestep = range(0, 12))
    coords = pd.DataFrame({"lon":[-30], "lat":[50]})
    ds.regrid(coords)

Interpolating to a regular latlon grid
--------------------------------------

If you want to interpolate to a regular latlon grid, you can use
``to_latlon``. ``lon`` and ``lat`` specify the minimum and maximum
longitudes and latitudes, while ``res``, a 2 variable list specifies the
resolution. For example, if we wanted to regrid the globe to 0.5 degree
north-south by 1 degree east-west resolution, we could do the following:

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds.select(timestep = 0)
    ds.to_latlon(lon = [-79.5, 79.5], lat = [0.75, 89.75], res = [1, 0.5])

Interpolating to another dataset’s grid
---------------------------------------

If we are working with two datasets and want to put them on a common
grid, we can interpolate one onto the other’s grid. We can illustate
this with a dataset of global sea surface temperature. Let’s start by
regridding the first timestep in this dataset to a regular latlon grid
covering the North Atlantic.

.. code:: ipython3

    ds1 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds1.select(timestep = 0)
    ds1.to_latlon(lon = [-79.5, 79.5], lat = [-0.75, 89.75], res = [1, 0.5])

We can then use this new dataset as the target grid in ``regrid``. So

.. code:: ipython3

    ds2 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds2.select(timestep = 0)
    ds2.regrid(ds1)



This method will also work using netCDF files. So, if you wanted you can
also use a path to a netCDF file as the target grid.


How to reuse the weights for regridding
---------------------------------------

Under the hood nctoolkit regrids data by first generating a weights file. There are situations where you 
will want to be able to re-use these weights. For example, if you are post-processing a large number of files
one after the other. To make this easier nctoolkit let's you recycle the regridding info. This let's you interpolate
using either ``regrid`` or ``to_latlon``, but keep the regridding data for future use by ``regrid``.

The example below illustrates this. First, we regrid a global dataset to a regular latlon grid covering the North Atlantic, setting the recycle argument to True.

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds.select(timestep = 0)
    ds.to_latlon(lon = [-79.5, 79.5], lat = [-0.75, 89.75], res = [1, 0.5], recycle = True)

We can then use the grid from data for regridding:

.. code:: ipython3

    ds1 = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds1.select(timestep = 0)
    ds1.regrid(ds)

This, of course, requires that the grids in the datasets are consistent. If you want to access the weights and grid files generated, you can do the following:

.. code:: ipython3
    ds._weights
    ds._grid

These files are deleted either when ``data`` is deleted or when the Python session is existed.

Resampling
----------

If you want to make data more coarse spatially, just use the
``resample_grid`` method. This will, for example, let you select every
2nd grid grid cell in a north-south and east-west direction. This is
illustrated in the example below, where a dataset which has spatial
resolution of 1 by 1 degrees is coarsened, so that only every 10th cell
is selected in a north-south and east-west. In other words it is now a
10 degrees by 10 degrees dataset.

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
    ds.select(timestep = 0)
    ds.resample_grid(10)

Vertical interpolation
----------------------

We can carry out vertical interpolation using the ``vertical_interp``
method. This is particularly useful for oceanic data. This is
illustrated below by interpolating ocean temperatures from NOAA’s World
Ocean Atlas for January to a depth of 500 metres. The
``vertical_interp`` method requires a ``levels`` argument, which is
sea-depth in this case.

.. code:: ipython3

    ds = nc.open_thredds("https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/temperature/A5B7/1.00/woa18_A5B7_t01_01.nc")
    ds.select(variables="t_an")
    ds.vertical_interp(levels= [500])

