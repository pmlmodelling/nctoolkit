News
============

Release of v0.9.2
---------------

Version 0.9.1 will be released in April 2023. This release will contain a new method for producing high quality static plots.

A new method, `set`, will be introduced that will make it easier to rename variables, and change units and long names etc.

Some improvements will be made to internals.

Release of v0.9.1
---------------

Version 0.9.1 was released on the 19th of April 2023. This was a quick release to deal with some breaking changes to add/subtract etc. methods due to the release of pandas 2.0.0.

Release of v0.9.0
---------------

Version 0.9.0 was released on 2nd March 2023. This is a major(ish) release with some breaking changes related to plotting.

On pypi, cartopy has been switched to an optional dependency because it was causing installation difficulties for some users. You can now do a "complete" installation using pip to get all optional dependencies::

    $ pip install nctoolkit[complete]

This does not impact the conda version, which will behave as before.

Support is now available for Python 3.11.

File paths with spaces are now supported. 





Release of v0.8.6
---------------

Version 0.8.6 was released on 23rd December 2022. This is a minor releases that tidies up some issues and has some method enhancements.

The `regrid` and `to_latlon` methods can now be more efficient for multi-file datasets where all files have the same grid. Previously, the methods identified the grids for all methods. You 
can now set the `one_grid` argument to `True`, which will result in the methods assuming all files have the same grid, and only the first file being checked.

There was an issue with multi-file datasets in parallel in Python 3.8 and 3.9. A confusing TypeError was being thrown due to signalling issues by multiprocessing. This gave the impression there was
a problem with processing when there wasn't one. This problem is now fixed.


Release of v0.8.5
---------------

Version 0.8.5 was released on 14th December 2022. This is a minor release that deals with clean up issues on Jupyter notebooks. A change in a recent version of ipykernel was causing nctoolkit to not automatically remove
temporary files on exit, though only in jupyter notebooks. This should now be fixed.

The `annual_anomaly` method now lets users temporally align the output, in the same way as other temporal methods such as `roll_mean`.

Some improvements have been made to internals for better warnings and errors.



Release of v0.8.4
---------------

Version 0.8.4 was released on 6th  December 2022.

This update improves the ability to handle missing values. A method iss introduced for changing the fill value missing values, `set_fill`.

Another method `missing_as` is introduced. This will do the opposite of `as_missing`. Instead of setting a range of values to missing values, it will set missing values to a constant value.

Dataset contents will now show the fill value for variables. Furthermore, `open_data` will now check if the fill value is zero, which can cause problems for logical comparisons etc.


Release of v0.8.2
---------------

Version 0.8.2 was released on 25h November 2022. This release changed plotting so that it does not show coastlines by default.

Plotting with coastlines was causing plotting to crash on some systems due to issues with how nctoolkit's Python dependencies work with non-Python dependencies. Essentially plotting could crash if cartopy and pyproj were importable, but not fully functional. These were not a problem with nctoolkit installations from conda, which will install non-Python dependencies, but some non-conda insttallations would no longer plot maps as a Python dependency could be incompatible with the non-Python dependencies on user systems.

If you want to plot the coastline, do the following:

`ds.plot(coast=True)`

This is not an ideal fix, but it was necessary as a high proportion of users have a semi-functional cartopy installation, and there is no way for them to know that this is causing the plotting problem. A future release will hopefully provide automatic coastlines when cartopy and pyproj are fully functional on people's systems.

Release of v0.8.0
---------------

Version 0.8.0 was released on 17th November 2022. This was a major release that introduces some breaking changes.

The major improvement in this release is to vertical methods. All vertical methods should now work with files with vertical axes
that are either consistent or vary spatially. Before some methods only worked with z-levels, i.e. files with fixed vertical levels. This
change will result in a requirement that `vertical_mean`, `vertical_interp` and `vertical_integration` need users to specify whether the vertical
levels are fixed spatially, using the fixed arg.


There were also some improvements to internals.





Release of v0.7.6
---------------


Release data: 30th September 2022.

This is a minor release that significantly simplifies basic arithmetic and logical operations.

Simple methods such as +, - etc. can now use standard python syntax.

For example, if you wanted to add 2 to a dataset you can now do the following:

`ds.add(2)`

as this instead

`ds+2`

The same goes for logical operators. You can do the following to identify if the values in a datset are below 2:

`ds<2`

whereas you previously had to do this:

`ds.compare("<2")`

Note: because nctoolkit methods only modify datasets and do not return datasets, the following will not work:

`ds1+ds2+2`

Instead, you would need to do:

`ds1+ds2`
`ds1+2`

Release of v0.7.1
---------------

Release data: 10th September 2022.

This is a major release with some breaking changes.

The deprecated `select` method has now been removed. Users should now use the `subset` method.

A progress bar will now display when processing large datasets. This will only show when nctoolkit thinks something will take a while. If you want to always show a progress
bar for multi-file datasets, you can do this: `nc.options(progress = 'on')`.




Release of v0.6.0
---------------

Release date: 15th August 2022. 

This is a major release that introduces some breaking changes. All methods that carry out temporal averaging of any sort will now align output times to the right. This applies to methods such as
`tmean` and `rolling_mean`. The internals when `align = "left"` option have been modified, as the CDO call was sometimes giving incorrect results. 



Release of v0.5.4
---------------

This is a minor release on August 10th 2022.  

It improves the abilities of temporal methods, giving users the ability to select how they want times in output to be aligned.

For example, if you are calculating a rolling mean, you might want the output times to be the first, middle or final time in the temporal window. This release
will add that ability to nctoolkit's temporal methods. Previously nctoolkit used CDO's default methods, and did not allow users to do anything else.  By default, output dates will be aligned to the middle.

The `match_points` methods were throwing an error when there were non-unique vertical values. This is now fixed.


Some improvements have been made to package internals. 





Release of v0.5.1
---------------

This was a minor release made on 30th June 2022. It includes method enhancements.

The `subset` method now allows negative time slicing.

The `set_missing` method is deprecated and replaced with a less ambiguously named `as_missing` method.

The `plot` method will no longer show a plot title by default to make things cleaner.

The `vertical_integration` method now works with multi-file datasets and will not calculate vertical integrations for the thickness variable.

Some improvements have been made to improve error messages, and the `check` method now checks for data type of time.

A new method ``as_type`` has been added for changing data type of individual variables and coordinates.



Release of v0.5.0
---------------

This relase was made on 13th June 2022. The `match_points` method now allows extrapolation to vertical depths. 

Release of v0.4.9
---------------

This relase was made on 9th June 2022. The `subset` method now accepts levels.

Release of v0.4.8
---------------

This release improves temporal merging of large datasets. Previously on some systems this would fail on datasets made up of more than 1,000 files due to system limits. Under the hood, nctoolkit now deals with this.

The merge method also now contains a check argument that can be used to speed up merging of large datasets when you know the files can be merged problem-free. Previously, merge always checked if files being merged had the same variables when doing a temporal merge. This can now be switched off if you are confident this does not need to happen.


Release of v0.4.7
---------------

Version 0.4.7 was released on June 5th 2022.

This release contained a new method called match_points that can do matchups with a spatiotemporal dataframe.





Release of v0.4.6
---------------

Version 0.4.6 was released on June 3rd 2022.

This release will enhance existing methods.

The ``select`` method will be replaced by ``subset``. This behave in the way same way as ``select``, but will also allow users to subset data base on longitude and latitude using the ``lon`` and ``lat`` as args.

The export methods ``to_nc``, ``to_xarray`` and ``to_dataframe`` now allow only a subset of the data to be exported. Additional arguments can be sent to the methods, which will then be sent to the ``subset`` method.

The new matchpoint methods for matching netCDF and point data have been smoothed out with additional options.


Minor bug fix:  The weighted in datasets with recycled regridding weights were not copied properly. This is now fixed.

Release of v0.4.5
---------------

Version 0.4.5 was released in late May 2022. This was a minor release that fixed an issue with ``ds.variables`` when there were a) many variables and b) CDO version above 2.0.0.

Release of v0.4.4
---------------

Version 0.4.4 was released in late May 2022.

This version introduces a new class called `Matchpoint` which will allow automated matchups between netCDF files and point observations in pandas dataframes. This class is created using ``nc.open_matchpoint``. Matchups are generated by using the ``add_data``, ``add_points``, ``add_depths``, and ``matchup`` methods.

For datasets, ``ds`` now provides a more informative summary of dataset contents.

The ``split`` method now automatically sorts the files, so that they are sorted by date when temporal splitting occurs. 

The methods ``surface``, ``merge_time`` and ``tvariance``` have been removed after periods of deprecation. Use ``top``, ``merge`` and ``tvar`` instead.


Release of v0.4.3
---------------


Version 0.4.3 was released in May 2022. This is release with some new methods, improvements to internals some bug fixes. Code written for previous 0.4x versions of nctoolkit will be compatible.

This version will be compatible with CDO versions 2.0.5x.

A new function ``open_geotiff`` will allow GeoTiff files to be opened. This is a wrapper around rioxarray, which will convert the GeoTiff to NetCDF. It will require rioxarray to be installed.

A new method ``surface_mask`` has been added to enable identifying top levels with data in cases when there are missing values in the actual top level.

A new method ``is_corrupt`` has been added. This can identify whether NetCDF files are likely to be corrupt. Under-the hood, methods will now suggest running ``is_corrupt`` when system errors imply the files are corrupt. 

The methods ``to_xarray`` and ``to_dataframe`` no long accept the `cdo_times` argument, as this has essentially been redundant for a few nctoolkit versions. 

The ``plot`` method now lets users send kwargs to hvplot to make customizations, such as log-scales an option. This will require the latest version of ncplot.

The ``select`` method now lets user select days of month, using ``ds.select(day = 1)``.

The ``split`` method now allows splitting by timestep using ``split("timestep")``.



Release of v0.4.2
---------------

Version 0.4.2 was released in March 2022.

This is a minor release with a couple of method enhancements. Plots can now be saved to html files using the `out` arguments. The ``nco_command`` method now works over multiple cores when these are set using ``nc.options``.



Release of v0.4.1
---------------

Version 0.4.1 was released in March 2022. This is a minor release focusing on improving nctoolkit internals.

A new method, called ``check`` is introduced that can be used to troubleshoot data problems and to ensure there are no obvious data issues (such as a lack of CF-compliance).

Users can now access dataset calendars using ``ds.calendar``.

The ``drop`` method now lets you remove time steps using the ``times`` argument.

The dataset attribute `variables_detailed` is now removed after being replaced by `contents` in version 0.3.9.

This version will recommend CDO versions greater than 1.9.7, because ensuring nctoolkit compatibility with earlier versions was becoming difficult and likely of little need to users.

Some coding improvements have enhanced the performance of the ``add``, ``subtract`` etc. methods.

Bug fixes: The methods ``multiply`` etc. failed when datasets did not have time as a dimension in version 0.4.0. This is now fixed. Previously, `ds.contents` always returned None for the number of time steps. Now fixed.


Release of v0.4.0
---------------

Version 0.4.0 was released in January 2022. This is a major release that features some breaking changes. Methods for adding, subtracting, multipling and substracting datasets from each other will be enhanced. Until now these methods used a simplistic approach values from matching time steps were added to each other, etc. So if you are subtracting a 12 time step file from a dataset, only the first 12 time steps were subtracted from. However, often this is not what you want. For example, you might want to subtract yearly months from a file which contains montly values for each year. 

This version of nctoolkit updates these methods so that it can figure out what kind of addition etc. it should carry out. For example, if you have a dataset which has monthly values for each year from 1950 to 1999, and use ``subtract`` to subtract the values from a file which contains annual means for each year from 1950, it will subtract the annual mean for 1950 from each month in 1950 and the the annual mean for 1951 from each month in 1951, and so on. 

Users are now able to specify the numeric precision of datasets using ``ds.set_precision``. By default uses the underlying netCDF file's data type. This is normally not a problem. However, when the data type is integer, this can cause problems. ``nc.open_data`` has been updated with this issue in mind. It will now warn users when the data type of the netCDF is integer, and it suggested switching to float 'F64' or 'F32'.

The ``drop`` method has been enhanced. It now accepts day, month and year as arguments to enable dropping specific time periods. For example ``ds.drop(month = 2, day = 29)`` will remove leap days. Code written to use the old ``drop`` method will now fail, as keywords are now required.

The method ``surface`` has now been renamed ``top`` for consistency with ``bottom``. ``surface`` is deprecated and will be removed in a few months.

The ``split`` method now allows users to split datasets into multiple files by variable.

``ds.times`` now returns a datetime object, not a str as before.




Release of v0.3.9
---------------

Version 0.3.9 was released in November 2021. This is minor release focusing on under-the-hood improvements and new methods.

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







