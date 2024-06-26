import nctoolkit as nc
import pandas as pd
import platform
import xarray as xr
import os, pytest

nc.options(lazy=True)
if platform.system() == "Linux":
    nc.options(parallel = False)

ff = "data/sst.mon.mean.nc"


class TestOne:
    def test_clim1(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.split("year")
        tracker.ensemble_mean(nco=True)
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff, checks = False)
        tracker.tmean(["month"])
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == -1.5543334484100342 
        assert x == y

        n = len(nc.session_files())
        assert n == 1

#    def test_clim2(self):
#        tracker = nc.open_data(ff, checks = False)
#        tracker.split("year")
#        tracker.crop(lon=[50, 60])
#        tracker.ensemble_mean(nco=True)
#        tracker.spatial_mean()
#        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
#        tracker = nc.open_data(ff, checks = False)
#        tracker.tmean("month")
#        tracker.crop(lon=[50, 60])
#        tracker.spatial_mean()
#        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
#        assert x == 20.050094604492188
#        assert x == y
#        print(nc.session_files())
#
#        n = len(nc.session_files())
#        assert n == 1
#
#    def test_cdocommand(self):
#        tracker = nc.open_data(ff, checks = False)
#        tracker.subset(months = 1)
#        tracker.spatial_mean()
#        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
#        tracker = nc.open_data(ff, checks = False)
#        tracker.cdo_command("cdo selmon,1")
#        tracker.spatial_mean()
#        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
#
#        n = len(nc.session_files())
#        assert n == 1
#
#        assert x == y
#
#    def test_percentile(self):
#        tracker = nc.open_data(ff, checks = False)
#        tracker.crop(lon=[50, 60])
#        tracker.tpercentile(50)
#        tracker.spatial_mean()
#        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
#        assert x == 19.71255874633789
#
#        n = len(nc.session_files())
#        assert n == 1
#
#    def test_empty(self):
#        n = len(nc.session_files())
#        assert n == 0
