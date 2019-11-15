import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.lazy()
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
tracker.release()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")
y = len(tracker.history)

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.split("year")
n_files = len(tracker.current)
tracker.merge_time()
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")


ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.split("year")
n_files = len(tracker.current)
tracker.lazy()
tracker.merge_time()
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
tracker.release()
y = len(tracker.history)
x = tracker.to_xarray().sst.values[0][0][0].astype("float")

ff = nc.create_ensemble("data/ensemble/")
tracker = nc.open_data(ff)
tracker.mean()
tracker.ensemble_mean()
tracker.spatial_mean()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.lazy()
tracker.transmute({"sst":"sst+273.15"})
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
tracker.transmute({"sst":"sst-273.15"})
tracker.release()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")
y = len(tracker.history)

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.lazy()
tracker.mutate({"sst1":"sst+273.15"})
tracker.select_years(list(range(1950, 1959))) 
tracker.select_months([1,2,3,4,5])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_mean()
tracker.mean()
tracker.spatial_mean()
tracker.transmute({"sst2":"sst1-273.15"})
tracker.release()
x = tracker.to_xarray().sst2.values[0][0][0].astype("float")
y = len(tracker.history)

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.seasonal_mean_climatology()
tracker.select_months(2)
tracker.spatial_mean()
x = tracker.to_xarray().sst.values[0][0][0].astype("float")

ff = "data/sst.mon.mean.nc"
tracker1 = nc.open_data(ff)
tracker2 = nc.open_data(ff)
tracker2.rename({"sst": "tos"})
tracker = nc.merge(tracker1, tracker2)
tracker.transmute({"bias":"sst-tos"})
tracker.mean()
tracker.spatial_mean()
x = tracker.to_xarray().bias.values[0][0][0].astype("float")

ff = "data/sst.mon.mean.nc"
tracker = nc.open_data(ff)
tracker.select_years(list(range(1950, 1959)))
tracker.select_months([1,2,3,4,5])
tracker.select_months([1,2,3,4,5,6])
tracker.clip(lon = [0,90])
tracker.clip(lat = [0,90])
tracker.annual_anomaly(baseline = [1950, 1979])
x = (os.path.exists(tracker.current))
