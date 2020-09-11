import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestSeasst:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(1980)
        tracker.seasonal_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == -1.6950000524520874
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(1980)
        tracker.seasonal_min()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == -1.7020000219345093
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(1980)
        tracker.seasonal_max()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == -1.6880000829696655
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(1980)
        tracker.seasonal_range()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 0.01399993896484375
        n = len(nc.session_files())
        assert n == 1
