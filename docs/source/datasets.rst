Datasets
========

nctoolkit works with what it calls datasets. Each dataset is made up of
or more netCDF files. 

Opening datasets
----------------

There are 3 ways to create a dataset: ``open_data``, ``open_url`` or
``open_thredds``.

If the data you want to analyze that is available on your computer
use ``open_data``. This will accept either a path to a single file or a
list of files. It will also accept wildcards. So if you wanted to open
all of the files in a folder called data as a dataset, you could do the following:

.. code:: ipython3

    ds = nc.open_data("data/*.nc")

If you want to use data that can be downloaded from a url, just use
``open_url``. This will download the netCDF files to a temporary folder,
and it can then be analyzed.


If you want to analyze data that is available from a thredds server or opendap,
then user ``open_thredds``. The file paths should end with .nc.

Visualization of datasets
-------------------------

You can visualize the contents of a dataset using the ``plot`` method.
Below, we will plot temperature for January and the North Atlantic:

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    ds.plot()

Please note there may be some issues due to bugs in nctoolkit's dependencies that cause problems plotting some data
types. If data does not plot, raise an issue `here <https://github.com/pmlmodelling/nctoolkit/issues>`_.

Modifying datasets and lazy evaluation
---------------------------


nctoolkit works by performing operations and then saving the results as either a temporary file or in
a file specified by the user. We can illustrate this with the following code. This will select the first time
step from a file available over thredds and will plot the results. 

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    ds.select(time = 0)
    ds.plot()

You will notice, once this is done, that the file associated with the dataset is now a temporary file.

.. code:: ipython3

    ds.current

This will happen each time nctoolkit carries out an operation. This is potentially an invitation to slow-running code. You do not want to
be constantly reading and writing data. Ideally, you want a processing chain which minimizes IO. nctoolkit 
enables this by allowing method chaining, thanks to the method chaining of its computational back-end CDO.

Let's look at this chain of code:


.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    ds.assign(sst = lambda x: x.sst + 273.15)
    ds.select(months = 1)
    ds.crop(lon = [-80, 20], lat = [30, 70])
    ds.spatial_mean()


What is potentially wrong with this? It carries out four operations, so we absolutely do not want to create 
temporary file in each step. So instead of evaluating the operations line by line nctoolkit only evaluates
them either when you tell it to or it has to. So in the code example above we have told nctoolkit what to do to that dataset,
but have not told it to actually do any of it.

The quickest way to evaluate everything using ``run``. The code above would become: 

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    ds.assign(sst = lambda x: x.sst + 273.15)
    ds.select(months = 1)
    ds.crop(lon = [-80, 20], lat = [30, 70])
    ds.spatial_mean()
    ds.run()


Evaluation is, to use the technical term, lazy within nctoolkit. It only evaluates things until it needs to
or is forced to. 

This allows us to create efficient processing chain where we read the input file and write to the output file with no
intermediate file writing. If, in the example above, we wanted to save the output file, we could do this:

.. code:: ipython3

    ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE/data.mon.ltm.1981-2010.nc")
    ds.select(months = 1)
    ds.crop(lon = [-80, 20], lat = [30, 70])
    ds.spatial_mean()
    ds.to_nc("foo.nc")


List-like behaviour of datasets
-------------------------

If you want to view the files within a dataset view the ``current`` attribute. 

.. code:: ipython3
    ds.current

This is a list that gives the file(s) within the dataset. To make processing these files easier nctoolkit
features a number of methods similar to lists.

First, datasets are iterable. So, you can loop through each element of a dataset as follows:


.. code:: ipython3
    for ff in ds:
        # do something with ff

You can find out how many files are in a dataset, using ``len``:

.. code:: ipython3
   len(ds)

You can add a new file to a dataset using ``append``:

.. code:: ipython3
    ds.append("foo.nc") 

This method also let you add the files from another dataset.

Similarly, you can remove files from a dataset using ``remove``:

.. code:: ipython3
    ds.remove("foo.nc") 

In line with typical list behaviours, you can also create empty datasets as follows:

.. code:: ipython3
    ds = nc.open_data() 


This is particularly useful if you need to create an ensemble based on multiple files that need significant processing before being added to the dataset.



Dataset attributes
------------------

We can find out key information about a dataset using its attributes.

If we want to know the variables available in a dataset called ds, we would do:

.. code:: ipython3

    ds.variables

If we want to know the vertical levels available in the dataset, we use the following. 

.. code:: ipython3

    ds.levels

If we want to know the files in a dataset, we would do this. nctoolkit works by generating temporary files,
so if you have carried out any operations, this will show a list of temporary files.

.. code:: ipython3

    ds.current

If we want to find out what times are in the dataset we do this:

.. code:: ipython3

    ds.times

If we want to find out what months are in the dataset:

.. code:: ipython3

    ds.months

If we want to find out what years are in the dataset:

.. code:: ipython3

    ds.years

We can also access the history of operations carried out on the dataset. This will show the operations 
carried out by nctoolkit's computational back-end CDO:

.. code:: ipython3

    ds.history












