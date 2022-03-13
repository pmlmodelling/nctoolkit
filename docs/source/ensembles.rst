Multi-file methods
==================

nctoolkit is built to handle multi-file datasets easily and efficiently.
Parallel processing of files, ensemble averaging and merging are all
easily done.

To create a multi-file dataset, you just need to supply a list of files
to ``open_data``. Alternatively, you can use wild cards. The following
will create a multi-file dataset with all of the files in the foo
folder:

.. code:: ipython3

    import nctoolkit as nc
    ds = nc.open_data("foo/*.nc")

Standard nctoolkit methods can then be applied to each file within the
ensemble. For example, if we wanted a temporal mean of each file, we
would do the following:

.. code:: ipython3

    ds.tmean()

Note, to avoid any confusion: this operation will only apply to
individual members of the multi-file dataset. We will later discuss
ensemble methods such as ``ensemble_mean``, which let you calculate
statistics across the ensemble.

Merging multi-file datasets
---------------------------

There are two ways to merge mult-file datasets, time-based and
variable-based.

Merging by time is done as follows:

.. code:: ipython3

    ds.merge("time")

This will join files together so that their times join up. It should be
used when files have the same variables and grids, but distinct times.

The second merging method is joining variables. In this case files
should have the same time steps or one file should have at most one time
step. This is done as follows:

.. code:: ipython3

    ds.merge("variable")

By default, nctoolkit uses variable-based merging.

Speeding up multi-file processing
---------------------------------

If you have access to multiple cores, it is very easy to ensure files
within a multi-file dataset are processed in parallel. Just set the
number of cores to be used. In the following case, we set it to 6:

.. code:: ipython3

    nc.options(6)

This results in files being processed simultaneously with 6 cores.

If you are working on multi-file datasets, it is almost always much
faster to set the number of cores to a high number and carry out
operations on the files before merging them using ``merge`` and not the
other way round.

Ensemble statistics
-------------------

In some cases, you will want to calculate averages etc. across the
multi-file dataset. For example, each file in a dataset could be from a
different climate model and you might simply the mean value across them.
This is very easily done. We can just calculate the ensemble mean as
follows:

.. code:: ipython3

    ds.ensemble_mean()

This will calculate the mean for each time step. For example, if you
have an ensemble which is made of monthly projections of temperature
from 20 different climate models, ``ensemble_mean`` will calculate the
monthly mean of those 20 models.

Multiple ensemble methods are available: ``ensemble_mean``,
``ensemble_percentile``, ``ensemble_stdev``, ``ensemble_var``,
``ensemble_max``, ``ensemble_min``, ``ensemble_range`` and
``ensemble_sum``.
