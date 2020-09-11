import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestReduce:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_reduce(self):
        nc.options(lazy=False)
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.reduce_dims()
        n = len(tracker.times)
        assert n == 0
        nc.options(lazy=True)

    def test_reduce2(self):
        nc.options(lazy=True)
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.reduce_dims()
        tracker.run()
        n = len(tracker.times)
        assert n == 0
        nc.options(lazy=True)
