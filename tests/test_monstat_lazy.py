import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/2003.nc"


class TestMonst:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_mean()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")

        assert x == 283.1600036621094
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_min()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")

        assert x == 282.57000732421875
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_max()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")

        assert x == 283.72998046875
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_range()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")

        assert x == 1.160003662109375
        n = len(nc.session_files())
        assert n == 1
