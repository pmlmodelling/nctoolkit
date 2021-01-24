Datasets
========

nctoolkit works with what it calls datasets. Each dataset is made up of
a single or multiple NetCDF files. Each time you apply a method to a
dataset the NetCDF file or files within the dataset will be modified.

Opening datasets
----------------

There are 3 ways to create a dataset: ``open_data``, ``open_url`` or
``open_thredds``.

If the data you want to analyze is already available on your computer
use ``open_data``. This will accept either a path to a single file or a
list of files to create a dataset.

If you want to use data that can be downloaded from a url, just use
``open_url``. This will download the NetCDF files to a temporary folder,
and it can then be analyzed.

If you want to analyze data that is available from a thredds server,
then user ``open_thredds``. The file paths should end with .nc.

Dataset attributes
------------------

We can find out key information about a dataset using its attributes.
Here we will use a sea surface temperature file that is available via
thredds.

If we want to know the variables available in a dataset called data, we would do:

.. code:: ipython3

    data.variables

If we want to know the vertical levels available in the dataset, we use the following. This is
particularly useful for oceanic data.

.. code:: ipython3

    data.levels

If we want to know the files in a dataset, we would do this. nctoolkit works by generating temporary files,
so if you have carried out any operations, this will show a list of temporary files.

.. code:: ipython3

    data.current

If we want to find out what times are in the dataset we do this:

.. code:: ipython3

    data.times

If we want to find out what months are in the dataset:

.. code:: ipython3

    data.months

If we want to find out what years are in the dataset:

.. code:: ipython3

    data.years

We can also access the history of operations carried out on the dataset. This will show the operations 
carried out by nctoolkit's computational back-end CDO:

.. code:: ipython3

    data.history


Lazy evaluation of datasets
---------------------------

nctoolkit works by performing operations and then saving the results as either a temporary file or in
a file specified by the user. This is potentially an invitation to slow-running code. You do not want to
be constantly reading and writing data. Ideally, you want a processing chain which minimizes IO. nctoolkit 
enables this by allowing method chaining, thanks to the method chaining of its computational back-end CDO.

Let's look at this chain of code:


.. code:: ipython3

    data = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    data.assign(sst = lambda x: x.sst + 273.15)
    data.select(months = 1)
    data.crop(lon = [-80, 20], lat = [30, 70])
    data.spatial_mean()


What is potentially wrong with? It carries out four operations, so we absolutely do not want to create 
temporary file in each step. So instead of evaluating the operations line by line nctoolkit only evaluates
them either when you tell it to or it has to. 

We force the lines to be evaluated using ``run``:

.. code:: ipython3

    data.history

.. code:: ipython3

    data = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    data.select(months = 1)
    data.crop(lon = [-80, 20], lat = [30, 70])
    data.spatial_mean()
    data.run()


If we working in a Jupyter notebook, we could instead use ``plot`` at the end of the chain:

.. code:: ipython3

    data = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    data.select(months = 1)
    data.crop(lon = [-80, 20], lat = [30, 70])
    data.spatial_mean()
    data.plot()

This will force everything to be evaluated before plotting. 

An alternative will be to write to a results file at the end of the chain:

.. code:: ipython3

    data = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    data.select(months = 1)
    data.crop(lon = [-80, 20], lat = [30, 70])
    data.spatial_mean()
    data.to_nc("foo.nc")

This creates an ultra-efficient processing chain where we read the input file and write to the output file with no
intermediate file writing.

Visualization of datasets
-------------------------

You can visualize the contents of a dataset using the ``plot`` method.
Below, we will plot temperature for January and the North Atlantic:

.. code:: ipython3

    data = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    data.select(months = 1)
    data.crop(lon = [-80, 20], lat = [30, 70])
    data.plot()

Please note there may be some issues due to bugs in nctoolkit's dependencies that cause problems plotting some data
types. If data does not plot, raise an issue `here <https://github.com/pmlmodelling/nctoolkit/issues>`_.



List-like behaviour of datasets
-------------------------

Datasets can be made up of multi-files. To make processing these files easier nctoolkit features a number of methods similar to lists.

Datasets are iterable. So, you can loop through each element of a dataset as follows:



.. code:: ipython3
    for ff in data:
        # do something with ff

You can find out how many files are in a dataset, using ``len``:

.. code:: ipython3
   len(data)

You can add a new file to a dataset using ``append``:

.. code:: ipython3
    data.append("foo.nc") 

This method also let you add the files from another dataset.

Similarly, you can remove files from a dataset using ``remove``:

.. code:: ipython3
    data.remove("foo.nc") 











