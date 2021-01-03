Global settings
---------------

nctoolkit let’s you set global settings using options.

The most important and recommended to update is to set evaluation to
lazy. This can be done as follows:

.. code:: ipython3

    nc.options(lazy = True)

This means that commands will only be evaluated when either request them
to be or they need to be.

For example, in the code below the 3 specified commands will only be
calculated after it is told to ``run``. This cuts down on IO, and can
result in significant improvements in run time. At present lazy defaults
to False, but this may change in a future release of nctoolkit.

.. code:: ipython3

    nc.options(lazy = True)
    data.tmean()
    data.crop(lat = [0,90])
    data.spatial_mean()
    data.run()

If you are working with ensembles, you may want to change the number of
cores used for processing multiple files. For example, you can process
multiple files in parallel using 6 cores as follows. By default cores =
1. Most methods can run in parallel when working with multi-file
datasets.

.. code:: ipython3

    nc.options(cores = 6)

By default nctoolkit uses the OS’s temporary directories when it needs
to create temporary files. In most cases this is optimal. Most of the
time reading and writing to temporary folders is faster. However, in
some cases this may not be a good idea because you may not have enough
space in the temporary folder. In this case you can change the directory
used for saving temporary files as follows:

.. code:: ipython3

    nc.options(temp_dir = "/foo")
