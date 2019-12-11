.. currentmodule:: nchack


####################
API Reference
####################

Session options
------------------

.. autosummary::
   :toctree: generated/

   options


Reading/copying data
------------------

.. autosummary::
   :toctree: generated/

   open_data
   DataSet.copy

Accessing attributes
------------------

.. autosummary::
   :toctree: generated/

   DataSet.size
   DataSet.start
   DataSet.current
   DataSet.history

Plotting
------------------

.. autosummary::
   :toctree: generated/

   DataSet.plot


Variable modification 
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.rename
   DataSet.mutate
   DataSet.transmute
   DataSet.set_missing

Netcdf file attribute modification 
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.set_longnames
   DataSet.set_attributes
   DataSet.set_units
   DataSet.set_gridtype

Vertical/level methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.bottom
   DataSet.surface
   DataSet.vertical_interp
   DataSet.vertical_mean
   DataSet.vertical_min
   DataSet.vertical_max
   DataSet.vertical_range



Rolling methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.rolling_mean
   DataSet.rolling_min
   DataSet.rolling_max
   DataSet.rolling_sum
   DataSet.rolling_range



Evaluation setting
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.release


Cleaning functions
---------------------

.. autosummary::
   :toctree: generated/

   cleanup()
   deep_clean()

=======

Ensemble creation
---------------------

.. autosummary::
   :toctree: generated/

   create_ensemble
   generate_ensemble

Arithemetic methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.mutate
   DataSet.transmute

   DataSet.add
   DataSet.subtract
   DataSet.multiply
   DataSet.divide


Ensemble statistics
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.ensemble_percentile
   DataSet.ensemble_mean
   DataSet.ensemble_min
   DataSet.ensemble_max
   DataSet.ensemble_range


Subsetting operations
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.clip
   DataSet.select_months
   DataSet.select_season
   DataSet.select_years
   DataSet.select_variables
   DataSet.remove_variables


Time-based methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.set_date
   DataSet.select_months
   DataSet.select_season
   DataSet.select_years

Interpolation methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.regrid
   DataSet.time_interp


Masking methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.mask_lonlat



Summary methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.annual_anomaly
   DataSet.phenology

Statistical methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.sum
   DataSet.mean
   DataSet.min
   DataSet.cum_sum
   DataSet.percentile

   DataSet.cor_space
   DataSet.cor_time
   DataSet.spatial_mean
   DataSet.spatial_min
   DataSet.spatial_max
   DataSet.spatial_range

   DataSet.monthly_mean
   DataSet.monthly_min
   DataSet.monthly_max
   DataSet.monthly_range

   DataSet.daily_mean_climatology
   DataSet.daily_min_climatology
   DataSet.daily_max_climatology
   DataSet.daily_mean_climatology
   DataSet.daily_range_climatology

   DataSet.monthly_mean_climatology
   DataSet.monthly_min_climatology
   DataSet.monthly_max_climatology
   DataSet.monthly_range_climatology

   DataSet.annual_mean
   DataSet.annual_min
   DataSet.annual_max
   DataSet.annual_range

   DataSet.seasonal_mean
   DataSet.seasonal_min
   DataSet.seasonal_max
   DataSet.seasonal_range

   DataSet.seasonal_mean_climatology
   DataSet.seasonal_min_climatology
   DataSet.seasonal_max_climatology
   DataSet.seasonal_range_climatology



Seasonal methods
---------------------

.. autosummary::
   :toctree: generated/


   DataSet.seasonal_mean
   DataSet.seasonal_min
   DataSet.seasonal_max
   DataSet.seasonal_range


   DataSet.seasonal_mean_climatology
   DataSet.seasonal_min_climatology
   DataSet.seasonal_max_climatology
   DataSet.seasonal_range_climatology
   DataSet.select_season



Merging methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.merge
   DataSet.merge_time
   merge

Climatology methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.daily_mean_climatology
   DataSet.daily_min_climatology
   DataSet.daily_max_climatology
   DataSet.daily_mean_climatology
   DataSet.daily_range_climatology

   DataSet.monthly_mean_climatology
   DataSet.monthly_min_climatology
   DataSet.monthly_max_climatology
   DataSet.monthly_range_climatology

Splitting methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.split_year
   DataSet.split_year_month
   DataSet.split_day
   DataSet.split_season


Display methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.view
   DataSet.times
   DataSet.depths
   DataSet.numbers
   DataSet.years
   DataSet.months
   DataSet.levels

Output methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.write_nc
   DataSet.to_xarray
   DataSet.to_dataframe
   DataSet.zip

Miscellaneous methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.cell_areas
   DataSet.cdo_command











