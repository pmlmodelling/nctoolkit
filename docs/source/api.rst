.. currentmodule:: nchack


####################
API reference
####################

Reading netcdf data
------------------

.. autosummary::
   :toctree: generated/

   open_data

Accessing attributes
------------------

.. autosummary::
   :toctree: generated/

   NCData.start
   NCData.current
   NCData.history
   NCData.size
   NCData.run




Variable modification 
---------------------

.. autosummary::
   :toctree: generated/

   NCData.rename
   NCData.mutate
   NCData.transmute
   NCData.set_longname
   NCData.set_unit
   NCData.set_missing

Vertical/level methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.bottom
   NCData.surface
   NCData.vertical_interp
   NCData.vertical_mean
   NCData.vertical_min
   NCData.vertical_max
   NCData.vertical_range



Rolling methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.rolling_mean
   NCData.rolling_min
   NCData.rolling_max
   NCData.rolling_sum
   NCData.rolling_range



Evaluation setting
---------------------

.. autosummary::
   :toctree: generated/

   NCData.lazy
   NCData.release


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

   NCData.mutate
   NCData.transmute

Ensemble statistics
---------------------

.. autosummary::
   :toctree: generated/

   NCData.ensemble_percentile
   NCData.ensemble_mean
   NCData.ensemble_min
   NCData.ensemble_max
   NCData.ensemble_range


Subsetting operations
---------------------

.. autosummary::
   :toctree: generated/

   NCData.clip
   NCData.select_months
   NCData.select_season
   NCData.select_years
   NCData.select_variables
   NCData.remove_variables


Time-based methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.set_date
   NCData.select_months
   NCData.select_season
   NCData.select_years

Interpolation methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.regrid
   NCData.time_interp


Masking methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.mask_lonlat



Summary methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.anomaly_annual
   NCData.phenology

Statistical methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.sum
   NCData.mean
   NCData.min
   NCData.cum_sum

   NCData.cor_space
   NCData.cor_time
   NCData.spatial_mean
   NCData.spatial_min
   NCData.spatial_max
   NCData.spatial_range

   NCData.monthly_mean
   NCData.monthly_min
   NCData.monthly_max
   NCData.monthly_range

   NCData.daily_mean_climatology
   NCData.daily_min_climatology
   NCData.daily_max_climatology
   NCData.daily_mean_climatology
   NCData.daily_range_climatology

   NCData.monthly_mean_climatology
   NCData.monthly_min_climatology
   NCData.monthly_max_climatology
   NCData.monthly_range_climatology

   NCData.annual_mean
   NCData.annual_min
   NCData.annual_max
   NCData.annual_range

   NCData.seasonal_mean
   NCData.seasonal_min
   NCData.seasonal_max
   NCData.seasonal_range

   NCData.seasonal_mean_climatology
   NCData.seasonal_min_climatology
   NCData.seasonal_max_climatology
   NCData.seasonal_range_climatology



Seasonal methods
---------------------

.. autosummary::
   :toctree: generated/


   NCData.seasonal_mean
   NCData.seasonal_min
   NCData.seasonal_max
   NCData.seasonal_range


   NCData.seasonal_mean_climatology
   NCData.seasonal_min_climatology
   NCData.seasonal_max_climatology
   NCData.seasonal_range_climatology
   NCData.select_season



Merging methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.merge
   NCData.merge_time
   merge_trackers

Climatology methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.daily_mean_climatology
   NCData.daily_min_climatology
   NCData.daily_max_climatology
   NCData.daily_mean_climatology
   NCData.daily_range_climatology

   NCData.monthly_mean_climatology
   NCData.monthly_min_climatology
   NCData.monthly_max_climatology
   NCData.monthly_range_climatology

Splitting methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.split_year
   NCData.split_year_month
   NCData.split_day
   NCData.split_season


Display methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.view
   NCData.times
   NCData.depths
   NCData.numbers
   NCData.show_years
   NCData.show_months
   NCData.show_levels

Output methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.to_netcdf
   NCData.to_xarray
   NCData.zip

Miscellaneous methods
---------------------

.. autosummary::
   :toctree: generated/

   NCData.cell_areas
   NCData.cdo_command







