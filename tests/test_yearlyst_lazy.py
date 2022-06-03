import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestYearlyst:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmean("year")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmin()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmin("year")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmax()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tmax("year")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_annualsum(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tsum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.tsum("year")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.trange()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(years=1990)
        tracker.trange("year")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1
