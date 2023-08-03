Parallel processing
===================

nctoolkit is written to enable rapid processing and analysis of netCDF
files, and this includes the ability to process in parallel. Two methods
of parallel processing are available. First is the ability to carry out
operations on multi-file datasets in parallel. Second is the ability to
define a processing chain in nctoolkit, and then use the multiprocessing or multiprocess
package to process files in parallel using that chain. The multiprocessing package is not
compatible with nctoolkit internals on macOS, so the multiprocess package should be used instead.

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

Parallel processing using multiprocessing or multiprocess
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

We can illustrate the use of nctoolkit to post-process multiple files in parallel with a simple chain which will
convert files that have temperature in degrees Celsius and then convert them to Kelvin and also save the new outputs as separate files. 


First, we would define a function that can take the input file, carry out the necessary processing and then save the output file in a new directory.

In this case, the original file is in a directory called ensemble and we will put it in a new one called new.


.. code:: ipython3
    def process_chain(infile):
        '''
        This function takes a file, converts the temperature to Kelvin and then saves the output in a new directory
        '''

        # define the outfile name
        outfile = infile.replace('ensemble', 'new')
        # check if directory for outfile exists and create if not
        if not os.path.exists(os.path.dirname(outfile)):
            os.mkdir(os.path.dirname(outfile))
        ds = nc.open_data(infile)
        # convert to Kelvin
        ds.assign(tos = lambda x: x.sst + 273.15)
        # save the output
        ds.to_nc(outfile)


We now want to loop through all of the files in a folder, apply the
function to them and then save the results in a new folder called new. 

.. code:: ipython3
    # identify files in the ensemble directory 
    ensemble = nc.create_ensemble("ensemble")
    import multiprocessing as mp
    import os
    # on macOS, use:
    #import multiprocess as mp
    # create a pool of workers
    pool = mp.Pool(3)
    # apply the function to each file in the ensemble
    for ff in ensemble:
        pool.apply_async(process_chain, [ff])
    # close the pool and wait for the work to finish
    pool.close()
    # wait for the processes to finish
    pool.join()


The number 3 in this case signifies that 3 cores are to be used.

Please note that if you are working interactively or in a Jupyter
notebook, it is best to reset parallel as follows once you have stopped
any parallel processing:

.. code:: ipython3

    nc.options(parallel = False)

This is because of the effects of manually terminating commands on
multiprocessing lists, which nctoolkit uses when in parallel mode. This appears to be due to a book in multiprocessing, which is hard to avoid.
