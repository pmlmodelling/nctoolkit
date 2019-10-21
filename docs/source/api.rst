.. currentmodule:: nchack


####################
API
####################

Trackers
=======

Creating a tracker
------------------


.. autosummary::
   :toctree: generated/

   NCTracker
   open_data

Attributes
------------------

.. autosummary::
   :toctree: generated/

   NCTracker.start
   NCTracker.current
   NCTracker.history
   NCTracker.size
   NCTracker.run



Variable modification 
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.rename
   NCTracker.mutate
   NCTracker.transmute
   NCTracker.set_longname
   NCTracker.set_unit
   NCTracker.set_missing

Vertical/level methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.bottom
   NCTracker.surface
   NCTracker.vertical_interp
   NCTracker.vertical_mean
   NCTracker.vertical_min
   NCTracker.vertical_max
   NCTracker.vertical_range



Rolling methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.rolling_mean
   NCTracker.rolling_min
   NCTracker.rolling_max
   NCTracker.rolling_sum
   NCTracker.rolling_range



Evaluation setting
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.lazy
   NCTracker.release


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

   NCTracker.mutate
   NCTracker.transmute

Ensemble statistics
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.ensemble_percentile
   NCTracker.ensemble_mean
   NCTracker.ensemble_min
   NCTracker.ensemble_max
   NCTracker.ensemble_range


Subsetting operations
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.clip
   NCTracker.select_months
   NCTracker.select_season
   NCTracker.select_years
   NCTracker.select_variables
   NCTracker.remove_variables


Time-based methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.set_date
   NCTracker.select_months
   NCTracker.select_season
   NCTracker.select_years

Interpolation methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.regrid
   NCTracker.time_interp


Masking methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.mask_lonlat



Summary methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.anomaly_annual
   NCTracker.phenology

Statistical methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.sum
   NCTracker.mean
   NCTracker.min
   NCTracker.cum_sum

   NCTracker.cor_space
   NCTracker.cor_time
   NCTracker.spatial_mean
   NCTracker.spatial_min
   NCTracker.spatial_max
   NCTracker.spatial_range

   NCTracker.monthly_mean
   NCTracker.monthly_min
   NCTracker.monthly_max
   NCTracker.monthly_range

   NCTracker.daily_mean_climatology
   NCTracker.daily_min_climatology
   NCTracker.daily_max_climatology
   NCTracker.daily_mean_climatology
   NCTracker.daily_range_climatology

   NCTracker.monthly_mean_climatology
   NCTracker.monthly_min_climatology
   NCTracker.monthly_max_climatology
   NCTracker.monthly_range_climatology

   NCTracker.annual_mean
   NCTracker.annual_min
   NCTracker.annual_max
   NCTracker.annual_range

   NCTracker.seasonal_mean
   NCTracker.seasonal_min
   NCTracker.seasonal_max
   NCTracker.seasonal_range

   NCTracker.seasonal_mean_climatology
   NCTracker.seasonal_min_climatology
   NCTracker.seasonal_max_climatology
   NCTracker.seasonal_range_climatology



Seasonal methods
---------------------

.. autosummary::
   :toctree: generated/


   NCTracker.seasonal_mean
   NCTracker.seasonal_min
   NCTracker.seasonal_max
   NCTracker.seasonal_range


   NCTracker.seasonal_mean_climatology
   NCTracker.seasonal_min_climatology
   NCTracker.seasonal_max_climatology
   NCTracker.seasonal_range_climatology
   NCTracker.select_season



Merging methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.merge
   NCTracker.merge_time
   merge_trackers

Climatology methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.daily_mean_climatology
   NCTracker.daily_min_climatology
   NCTracker.daily_max_climatology
   NCTracker.daily_mean_climatology
   NCTracker.daily_range_climatology

   NCTracker.monthly_mean_climatology
   NCTracker.monthly_min_climatology
   NCTracker.monthly_max_climatology
   NCTracker.monthly_range_climatology

Splitting methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.split_year
   NCTracker.split_year_month
   NCTracker.split_day
   NCTracker.split_season


Display methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.view
   NCTracker.times
   NCTracker.depths
   NCTracker.numbers
   NCTracker.show_years
   NCTracker.show_months
   NCTracker.show_levels

Output methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.to_netcdf
   NCTracker.to_xarray
   NCTracker.zip

Miscellaneous methods
---------------------

.. autosummary::
   :toctree: generated/

   NCTracker.cell_areas
   NCTracker.cdo_command





