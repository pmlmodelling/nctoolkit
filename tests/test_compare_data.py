import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestCompare:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_gt(self):
        tracker = nc.open_data(ff)
        tracker.select(time = 0)
        tracker.gt(ff)

        x = tracker.to_dataframe().sst.values[0]

        assert x == 0
        n = len(nc.session_files())
        assert n == 1

