News
============

Release of v0.3.2 
---------------

Version 0.3.2 will be released in April/May 2021. This will be a minor release focusing on removing deprecated methods and some under the hood improvements.



Release of v0.3.1 
---------------

Version 0.3.1 was released in March 2021. This is a minor release that includes new methods, under-the-hood improvements and the removal of deprecated methods.

New methods are introduced for identifying the first time step will specific numerical thresholds are first exceeded or fallen below etc:
``first_above``, ``first_below``, ``last_above`` and ``last_below``. The thresholds are either single numbers or can come from a gridded dataset
for grid-cell specific thresholds.

Methods to compare a dataset with another dataset or netCDF file have been added: ``gt`` and ``lt``, which stand for 'greater than' and 'less than'.

Users are be able to recycle the weights calculated when interpolating data. This can enable much faster interpolation of multiple files with the
same grid.

The temporal methods replaced by ``tmean`` etc. have now been removed from the package. So ``monthly_mean`` etc. can no longer be used.


Release of v0.3.0 
---------------

Version 0.3.0 was released in February 2021. This will be a major release introducing major improvements to the package.

A new method ``assign``  is now available for generating new variables. This replaces the ``mutate`` and ``transmute``, which were 
place-holder functions in the early releases of nctoolkit until a proper method for creating variables was put in place.
``assign`` operates in the same way as the ``assign`` method in Pandas. Users can generate new variables using lambda functions.

A major-change in this release is that evaluation is now lazy by default. The previous default of non-lazy evaluation was designed
to make life slightly easier for new users of the package, but it is probably overly annoying for users to have to set evaluation
to lazy each time they use the package.

This release features a subtle shift in how datasets work, so that they have consistent list-like properties. Previously, the
files in a dataset given by the ```current``` attribute could be both a str or a list, depending on whether there was one or
more files in the dataset. This now always gives a list. As a result datasets in nctoolkit have list-like properties, with ```append``
and ``remove`` methods available for adding and removing files. ``remove`` is a new method in this release. As before datasets are iterable.

This release will also allow users to run nctoolkit in parallel. Previous releases allowed files in multi-file datasets to be 
processed in parallel. However, it was not possible to create processing chains and process files in parallel. This is now possible
in version thanks to under-the-hood changes in nctoolkit's code base.

Users are now able to add a configuration file, which means global settings do not need to be set in every session or in every script.







