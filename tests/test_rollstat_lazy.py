import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestRollstat:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.rolling_mean(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 18.077280044555664
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.rolling_max(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 20.302736282348633
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.rolling_min(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 16.211519241333008

        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.rolling_range(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 4.091217517852783
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 180.77279663085938
        n = len(nc.session_files())
        assert n == 1

    def test_float(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.rolling_sum(window="x")

        with pytest.raises(ValueError):
            tracker.rolling_sum()

        with pytest.raises(ValueError):
            tracker.rolling_sum(window=0)

        with pytest.raises(ValueError):
            tracker.rolling_sum(window=-1)

        n = len(nc.session_files())
        assert n == 0
