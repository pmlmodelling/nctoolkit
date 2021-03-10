Parallel processing
===================

nctoolkit is written to enable rapid processing and analysis of netCDF
files, and this includes the ability to process in parallel. Two methods
of parallel processing are available. First is the ability to carry out
operations on multi-file datasets in parallel. Second is the ability to
define a processing chain in nctoolkit, and then use the multiprocessing
package to process files in parallel using that chain.

Parallel processing of multi-file datasets
------------------------------------------

If you have a multi-file dataset, processing the files within it in
parallel is easy. All you need to is the following:

.. code:: ipython3

    nc.options(cores = 6)

This will tell nctoolkit to process the files in multi-file datasets in
parallel and to use 6 cores when doing so. You can, of course, set the
number of cores as high as you want. The only thing nctoolkit will do is
limit it to the number of cores on your machine.

Parallel processing using multiprocessing
-----------------------------------------

A common task is taking a bunch of files in a folder, doing things to
them, and then saving a modified version of each file in a new folder.
We want to be able to parallelize that, and we can using the
multiprocessing package in the usual way.

But first, we need to change the global settings:

.. code:: ipython3

    import nctoolkit as nc
    nc.options(parallel = True)

This tells nctoolkit that we are about to do something in parallel. This
is critical because of the internal workings of nctoolkit. Behind the
scenes nctoolkit is constantly creating and deleting temporary files. It
manages this process by creating a safe-list, i.e. a list of files in
use that should not be deleted. But if you are running in parallel, you
are adding to this list in parallel, and this can cause problems.
Telling nctoolkit it will be run in parallel tells it to switch to using
a type of list that can be safely added to in parallel.

We can use multiprocessing to do the following: take all of the files in
folder foo, do a bunch of things to them, then save the results in a new
folder:

We start with a function giving a processing chain. There are obviously
different ways of doing this, but I like to use a function that takes the
input file and output file:

.. code:: ipython3

    def process_chain(infile, outfile):
        data = nc.open_data(ff) 
        data.assign(tos = lambda x: x.sst + 273.15)
        data.tmean()
        data.to_nc(outfile)

We now want to loop through all of the files in a folder, apply the
function to them and then save the results in a new folder called new:

.. code:: ipython3

    ensemble = nc.create_ensemble("../../data/ensemble")
    import multiprocessing
    pool = multiprocessing.Pool(3)
    for ff in ensemble:
        pool.apply_async(process_chain, [ff, ff.replace("ensemble", "new")])
    pool.close()
    pool.join()

The number 3 in this case signifies that 3 cores are to be used.

Please note that if you are working interactively or in a Jupyter
notebook, it is best to reset parallel as follows once you have stopped
any parallel processing:

.. code:: ipython3

    nc.options(parallel = False)

This is because of the effects of manually terminating commands on
multiprocessing lists, which nctoolkit uses when in parallel mode.
