.. currentmodule:: nctoolkit


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

Merging or analyzing multiple datasets
------------------

.. autosummary::
   :toctree: generated/

    merge
    cor_time
    cor_space
    



Accessing attributes
------------------

.. autosummary::
   :toctree: generated/

   DataSet.variables
   DataSet.years
   DataSet.months
   DataSet.times
   DataSet.levels
   DataSet.size
   DataSet.current
   DataSet.history
   DataSet.start

Plotting
------------------

.. autosummary::
   :toctree: generated/

   DataSet.plot
   DataSet.view


Variable modification 
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.mutate
   DataSet.transmute
   DataSet.rename
   DataSet.set_missing
   DataSet.sum_all

NetCDF file attribute modification 
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.set_longnames
   DataSet.set_units

Vertical/level methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.surface
   DataSet.bottom
   DataSet.vertical_interp
   DataSet.vertical_mean
   DataSet.vertical_min
   DataSet.vertical_max
   DataSet.vertical_range
   DataSet.vertical_sum
   DataSet.vertical_cum_sum
   DataSet.invert_levels
   DataSet.bottom_mask



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

   DataSet.run


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

   DataSet.ensemble_mean
   DataSet.ensemble_min
   DataSet.ensemble_max
   DataSet.ensemble_percentile
   DataSet.ensemble_range


Subsetting operations
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.clip
   DataSet.select_variables
   DataSet.remove_variables
   DataSet.select_years
   DataSet.select_months
   DataSet.select_season
   DataSet.select_timestep

Time-based methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.set_date
   DataSet.select_months
   DataSet.select_season
   DataSet.select_years
   DataSet.shift_hours
   DataSet.shift_days

Interpolation methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.regrid
   DataSet.to_latlon
   DataSet.time_interp


Masking methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.mask_box



Summary methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.annual_anomaly
   DataSet.monthly_anomaly
   DataSet.phenology

Statistical methods
---------------------

.. autosummary::
   :toctree: generated/

   DataSet.mean
   DataSet.min
   DataSet.percentile
   DataSet.max
   DataSet.sum
   DataSet.range
   DataSet.var
   DataSet.cum_sum

   DataSet.cor_space
   DataSet.cor_time

   DataSet.spatial_mean
   DataSet.spatial_min
   DataSet.spatial_max
   DataSet.spatial_percentile
   DataSet.spatial_range
   DataSet.spatial_sum

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

   DataSet.zonal_mean
   DataSet.zonal_min
   DataSet.zonal_max
   DataSet.zonal_range


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

   DataSet.split


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
   DataSet.nco_command
   DataSet.compare_all
   DataSet.reduce_dims
   DataSet.reduce_grid











