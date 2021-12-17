import nctoolkit as nc

#nc.options(lazy=True)

import pandas as pd
import xarray as xr
import os, pytest
import subprocess


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


class TestLazy:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_select(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1979)))
        tracker.select(months=[1, 2, 3, 4, 5])
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 18.435571670532227
        n = len(nc.session_files())
        assert n == 1

    def test_lazy1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1979)))
        tracker.select(months=[1, 2, 3, 4, 5])
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        y = len(tracker.history)
        assert x == 18.435571670532227
        if cdo_version() in ["1.9.2", "1.9.3"]:
            assert y == 2
        else:
            assert y == 1
        n = len(nc.session_files())
        assert n == 1

    def test_split1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split(by="year")
        assert len(tracker.current) == 30
        tracker.merge_time()
        tracker.select(years=list(range(1970, 1979)))
        tracker.select(months=[1, 2, 3, 4, 5])
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        tracker.run()
        nc.cleanup()
        assert len(nc.session_files()) == 1

        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 18.435571670532227

    def test_mergetime1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split(by="year")
        n_files = len(tracker.current)
        tracker.merge_time()
        tracker.select(years=list(range(1970, 1979)))
        tracker.select(months=[1, 2, 3, 4, 5])
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        tracker.run()
        y = len(tracker.history)
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 18.435571670532227
        assert n_files == 30
        if cdo_version() in ["1.9.2", "1.9.3"]:
            assert y == 4
        else:
            assert y == 2
        n = len(nc.session_files())
        assert n == 1

    def test_ensemble_mean_1(self):
        ff = nc.create_ensemble("data/ensemble/")
        tracker = nc.open_data(ff)
        tracker.tmean()
        tracker.ensemble_mean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 18.0283203125
        n = len(nc.session_files())
        assert n == 1



    def test_seasonal_clim1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.tmean("season")
        tracker.select(months=2)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 17.9996280670166
        n = len(nc.session_files())
        assert n == 1

    def test_merge_rename(self):
        ff = "data/sst.mon.mean.nc"
        tracker1 = nc.open_data(ff)
        tracker2 = nc.open_data(ff)
        tracker2.rename({"sst": "tos"})
        tracker2.run()
        tracker = nc.merge(tracker1, tracker2)
        tracker.assign(bias=  lambda x: x.sst-x.tos)
        tracker.tmean()
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_xarray().bias.values[0][0][0].astype("float")
        assert x == 0
        n = len(nc.session_files())
        assert n == 2

    def test_anomaly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.crop(lon=[-80, 20], lat=[30, 80])
        tracker.annual_anomaly(baseline=[1970, 1979])
        tracker.spatial_mean()
        tracker.tmean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == 0.11958891153335571
        n = len(nc.session_files())
        assert n == 1

    def test_arithall(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.add(1)
        tracker.subtract(1)
        tracker.multiply(2)
        tracker.divide(2)
        tracker.spatial_mean()
        tracker.tmean()
        tracker.run()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff)
        tracker.spatial_mean()
        tracker.tmean()
        tracker.run()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        assert x == y
        n = len(nc.session_files())
        assert n == 1
