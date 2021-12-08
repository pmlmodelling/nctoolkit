News
============

Release of v0.4.0
---------------

Version 0.4.0 will be released in December 2021. This will be a major release that features some breaking changes. Methods for adding, subtracting, multipling and substracting datasets from each other will be enhanced. Until now these methods used a simplistic approach values from matching time steps were added to each other, etc. So if you are subtracting a 12 time step file from a dataset, only the first 12 time steps were subtracted from. However, often this is not what you want. For example, you might want to subtract yearly months from a file which contains montly values for each year. 

This version of nctoolkit updates these methods so that it can figure out what kind of addition etc. it should carry out. For example, if you have a dataset which has monthly values for each year from 1950 to 1999, and use ``subtract`` to subtract the values from a file which contains annual means for each year from 1950, it will subtract the annual mean for 1950 from each month in 1950 and the the annual mean for 1951 from each month in 1951, and so on. 

Users are now able to specify the numeric precision of datasets using ``ds.set_precision``. By default uses the underlying netCDF file's data type. This is normally not a problem. However, when the data type is integer, this can cause problems. ``nc.open_data`` has been updated with this issue in mind. It will now warn users when the data type of the netCDF is integer, and it suggested switching to float 'F64' or 'F32'.

The ``split`` method now allows users to split datasets into multiple files by variable.

``ds.times`` now returns a datetime object, not a str as before.




Release of v0.3.9
---------------

Version 0.3.9 was in November 2021. This is minor release focusing on under-the-hood improvements and new methods.

A new method, ``from_xarray`` is added for converting xarray datasets to nctoolkit datasets.

Methods for identifying how many missing values appear in datasets have been added: `na_count` and `na_frac`. These will identify the number or fraction of values that are missing values in each grid cell. The methods operate the same way as the temporal methods. So `ds.na_frac("year")` will result in what fraction of values are missing values each year.

Methods for better upscaling of datasets will be added: ``box_mean``, ``box_sum``, ``box_max``. This will allow you to upscale to, for example, each 10 by 10 grid box using the mean of that grid box. This is useful for upscaling things like population data where you want the upscaled grid boxes to represent the entirety of the grid box, not the centre.

Improvements to  ``merge`` have been made. When variables are not included in all files nctoolkit will now only merge those in each file in a multi-file dataset. Previously it threw an error.

Functions for finding the times and months in netCDF files are now available: ``nc_years`` and ``nc_months`.

The attribute ``variables_detailed`` has been changed to ``contents``. It will also now give the number of time steps available for each variable.

``cdo_command`` now allows users to specify whether the CDO command used is an ensemble method. Previously methods applied on a file by file basis.



Release of v0.3.8
---------------

Version 0.3.8 was released in October 2021. This is a minor release, focusing on under-the-hood improvements and introducing better handling of files with varying vertical layers.


A method, ``vertical_integration`` for calculating vertically integrated totals for netCDF data of the likes of oceanic data, where the vertical levels vary spatially, were introduced. ``vertical_mean`` has been improved and can now calculate vertical mean in cases where the cell thickness varies in space.

``merge_time`` is deprecated, and its functionality will be incorporated into ``merge``. So, following this release ensemble merging should use ``merge``.

``open_url`` is now able to handle multiple urls. Previously it could only handle one.

Some under-the-hood improvements have been made to ``assign`` to ensure that truth statements do not occassionally throw an error.




Release of v0.3.7
---------------

Version 0.3.7 was released in August 2021. This is a minor release.

New mathematical methods for simple operations on variables were added: ``abs``, ``power``, ``square``, ``sqrt``, ``exp``, ``log`` and ``log10``. These methods match numpy names.


Bug fixes: ``assign`` previously did not work with ``log10``. Now fixed.

``compare_all`` was deleted after a period of deprecation.



Release of v0.3.6
---------------

Version 0.3.6 was released in July 2021. This was a minor release.

New methods ``ensemble_var`` and ``ensemble_stdev`` were introduced for calculating variance and standard deviation across ensembles. The method ``tvariance`` will be deprecated and is now renamed ``tvar`` for naming consistency.



Release of v0.3.5
---------------

Version 0.3.5 was released in May 2021.

This is a minor release focusing on some under-the-hood improvements in performance and a couple of new methods. 

It drops support for CDO version 1.9.3, as this is becoming too time-consuming to continue given the increasingly low reward. 

A couple of new methods have been added. ``distribute`` enables files to be split up spatially into equally sized m by n rectangles.  ``collect`` is the reverse of ``distribute``. It will collect distributed data into one file.

In prior releases ``assign`` calls could not be split over multiple lines. This is now fixed.

There was a bug in previous releases where ``regrid`` did not work with multi-file datasets. This was due to the enabling of parallel processing with nctoolkit. The issue is now fixed. 

The deprecated methods ``mutate`` and ``assign`` have now been removed. Variable creation should use ``assign``.




Release of v0.3.4
---------------

Version 0.3.3 was released in April 2021. 

This was a minor release focusing on performance improvements, removal of deprecated methods and introduction of one new method.

A new method ``fill_na`` has been introduced that allows missing values to be filled with the distanced weighted average.

The methods ``remove_variables`` and ``cell_areas`` have been removed and are replaced permanently by ``drop`` and ``cell_area``.


Release of v0.3.2 
---------------

Version 0.3.2 was released in March 2021. This was a quick release to fix a bug causing ``to_nc`` to not save output in the base directory.


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







