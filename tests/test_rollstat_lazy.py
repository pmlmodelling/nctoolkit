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

    def test_var(self):
        ds = nc.open_data("data/2003.nc")
        ds.rolling_var(10)
        assert "cdo -runvar,10" == ds.history[0]
        ds = nc.open_data("data/2003.nc")
        ds.rolling_stdev(10)
        assert "cdo -runstd,10" == ds.history[0]

    def test_align(self):
        ds = nc.open_data("data/2003.nc")
        ds.subset(times = range(0, 20))
        ds.rolling_mean(7, align = "first")
        ds.run()
        assert [x.day for x in ds.times][0] == 1
        
        ds = nc.open_data("data/2003.nc")
        ds.subset(times = range(0, 20))
        ds.rolling_mean(7, align = "last")
        ds.run()
        assert [x.day for x in ds.times][0] == 7
        
        ds = nc.open_data("data/2003.nc")
        ds.subset(times = range(0, 20))
        ds.rolling_mean(7, align = "centre")
        ds.run()
        assert [x.day for x in ds.times][0] == 4

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.rolling_mean(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.rolling_mean(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        assert x == y 

        assert x == 18.087982177734375


        n = len(nc.session_files())


        assert n == 1

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.rolling_max(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 20.407316207885742  
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.rolling_min(window=10, align = "left")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 16.158565521240234 

        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.rolling_range(window=10, align = "right")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 3.8962974548339844 
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "centre")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 180.8798065185547 
        n = len(nc.session_files())
        assert n == 1

    def test_float(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "left")
        tracker.subset(years=1990)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.rolling_sum(window=10, align = "left")
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
