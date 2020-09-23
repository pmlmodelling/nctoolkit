Exporting datasets
------------------

nctoolkit has a number of built in methods for exporting data to NetCDF,
pandas dataframes and xarray datasets.

Save as a NetCDF
================

The method ``write_nc`` lets users export a dataset to a NetCDF file. If
you want this to be a zipped NetCDF file use the ``zip`` method before
to ``write_nc``. An example of usage is as follows:

.. code:: ipython3

    import nctoolkit as nc
    data = nc.open_data(infile)
    data.mean()
    data.zip()
    data.write_nc(outfile)

Convert to xarray Dataset
-------------------------

The method ``to_xarray`` lets users export a dataset to an xarray
dataset. An example of usage is as follows:

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_mean()
    ds = data.to_xarray()

Convert to pandas dataframe
---------------------------

The method ``to_dataframe`` lets users export a dataset to a pandas
dataframe.

.. code:: ipython3

    data = nc.open_data(infile)
    data.annual_mean()
    df = data.to_dataframe()
