Importing and exporting data
------------------

nctoolkit can work with data available on local file systems, urls and over thredds and OPeNDAP.


Opening single files and ensembles
================

If you want to import a single netCDF file as a dataset, do the following:


.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_data(infile)


The `open_data` function can also import multiple files. This can be done in two ways. If we have a list of files we can do the following:

.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_data(file_list)


Alternatively, `open_data` is capable of handling wildcards. So if we have a folder called data, we can import all files in it as follows:


.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_data("data/*.nc")



Opening files from urls/ftp 
================

If we want to work with a file that is available at a url or ftp, we can use the `open_url` function. This will start by downloading the file to a temporary folder, so that it can be analysed.

.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_url(www.foo.nc)


Opening data available over thredds servers or OPeNDAP 
================

If you want to work with data that is available over a thredds server or OPeNDAP, you can use the `open_thredds` method. This will require that the url ends with ".nc". 

.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_thredds(www.foo.nc)


Exporting datasets
================

nctoolkit has a number of built in methods for exporting data to netCDF, pandas dataframes and xarray datasets.

Save as a netCDF
================

The method ``to_nc`` lets users export a dataset to a netCDF file. If
you want this to be a zipped netCDF file use the ``zip`` method before
to ``to_nc``. An example of usage is as follows:

.. code:: ipython3

    ds = nc.open_data(infile)
    ds.tmean()
    ds.zip()
    ds.to_nc(outfile)


Convert to pandas dataframe
================

The method ``to_dataframe`` lets users export a dataset to a pandas
dataframe.

.. code:: ipython3

    ds = nc.open_data(infile)
    ds.tmean()
    df = ds.to_dataframe()


Interacting with xarray datasets
================

If you want to move between nctoolkit and xarray dataset, you can use ``from_xarray`` and ``to_xarray``.

The method ``to_xarray`` lets users export a dataset to an xarray
dataset. An example of usage is as follows:

.. code:: ipython3

    ds = nc.open_data(infile)
    ds.tmean()
    xr_ds = ds.to_xarray()

If you want to convert an xarray dataset to an nctoolkit dataset, you can just the ``from_xarray`` function, as follows:

.. code:: ipython3

    ds = nc.from_xarray(ds_xr)

Exporting subsets of data
================

If you want to only export a subset of the data you can do this by providing additional args to the ``to_nc``, ``to_xarray`` and
``to_dataframe`` methods. These args will then be sent to the ``subset`` method.

For example, if you only wanted to export the year 2000 to xarray, you would do the following:

.. code:: ipython3

    ds.to_xarray(year = 2000)

Or if you wanted a spatial subset of the data you could do this:

.. code:: ipython3

    ds.to_xarray(lon = [0, 90], lat = [0, 90])




