import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import numpy as np


class TestZip:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_zip1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_timesteps(0)
        tracker.run()
        new = tracker.copy()
        x = os.path.getsize(tracker.current)
        tracker.zip()
        tracker.run()
        y = os.path.getsize(tracker.current)
        assert 0.8 * x > y

        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        new.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]
        assert x == y

        nc.options(lazy = False)
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_timesteps(0)
        new = tracker.copy()
        x = os.path.getsize(tracker.current)
        tracker.zip()
        y = os.path.getsize(tracker.current)
        assert 0.8 * x > y
        nc.options(lazy = True)

    def test_zip2(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_timesteps(0)
        tracker.zip()
        tracker.run()
        new = tracker.copy()
        x = os.path.getsize(tracker.current)
        tracker.zip()
        print(tracker._zip)
        tracker.run()
        y = os.path.getsize(tracker.current)
        z = np.round(x / y, 1).astype("float")
        assert z == 1

        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        new.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y
