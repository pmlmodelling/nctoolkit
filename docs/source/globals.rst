Global settings
============

nctoolkit let’s you set global settings using options.

Setting the number of cores in use 
---------------

If you are working with ensembles, you will probably  to change the number of
cores used for processing multiple files. For example, you can process
multiple files in parallel using 6 cores as follows. 

.. code:: ipython3

    nc.options(cores = 6)

Setting the temporary directory to use 
---------------

By default nctoolkit uses the OS’s temporary directories when it needs
to create temporary files. In most cases this is optimal. Most of the
time reading and writing to temporary folders is faster. However, in
some cases this may not be a good idea because you may not have enough
space in the temporary folder. In this case you can change the directory
used for saving temporary files as follows:

.. code:: ipython3

    nc.options(temp_dir = "/foo")

Turning on or off progress bars
---------------

By default, nctoolkit will display a progress bar when it thinks a process will take a long time for a multi-file
dataset. If you always want a progress bar to display when calculations are being carried out on multi-file datasets, regardless 
of their size, you can do the following:

.. code:: ipython3

    nc.options(progress = 'on')

If you find the progress bar annoying or distracting, you can just do this:

.. code:: ipython3

    nc.options(progress = 'off')


Switching off lazy evaluation
---------------

By default evaluation in nctoolkit is lazy, so things are only evaluated when they have to be. If you want things to be evaluated each time a method
is used, you can do this:

.. code:: ipython3

    nc.options(lazy = False)


Setting global settings using a configuration file
---------------

You may want to set some global settings either permanently or on a project level.
You can do this by setting up a configruation file. This should be a plain text file called .nctoolkitrc or
nctoolkitrc. It should be placed in one of two locations: your working directory or your 
home directory. When nctoolkit is imported, it will look first in your working directory and
then in your home directory for a file called .nctoolkitrc or nctoolkitrc. It will then use
the first it finds to change the global settings from the defaults.

The structure of this file is straightforward. For example, if you wanted to set evaluation to
lazy and the number of cores used for processing multi-file datasets, you would the following in your configuration file:


    lazy : True 

    cores : 6 

The files roughly follow Python dictionary syntax, with the setting and value separate by :.  Note that unless the setting 
is specified in the file, the defaults will be used. If you do not provide a configuration file, nctoolkit will use the 
default settings.









