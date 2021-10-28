Backends
========

nctoolkit relies on Climate Data Operators (CDO) as its computational backend. This is a high-powered command line tool for manipulating and analyzing climate model data.
You can read more about CDO on their `website <https://code.mpimet.mpg.de/projects/cdo/>`_.

nctoolkit is designed as a stand alone package and users will require no understanding of CDO to use it. However, people with knowledge of CDO may want to use the ``cdo_command`` method
to use CDO methods directly.

Using CDO commands
----------------

If you want to apply a CDO command in nctoolkit, all you need to do is remove the beginning and end, i.e. 'cdo' and the file names.

So, a typical CDO command looks like this::


.. code:: ipython3

    cdo yearmean infile.nc outfile.nc 

If we wanted to use this in nctoolkit, we would just do this::


.. code:: ipython3

    ds.cdo_command("yearmean")


Using NCO commands
----------------

nctoolkit also allows you to apply NCO commands to datasets using the ``nco_command`` method. You just need to remove the two file names from the command you want to apply.

So, the following command::


.. code:: ipython3

    ncks -v kd_490 -d lat,40.0,70.0 -d lon,-20.0,15.0 infile.nc outfile.nc

would become::

.. code:: ipython3

    ds.nco_command("ncks -v kd_490 -d lat,40.0,70.0 -d lon,-20.0,15.0")


