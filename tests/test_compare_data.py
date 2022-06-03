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
        tracker.subset(time = 0)
        tracker.gt(ff)

        x = tracker.to_dataframe().sst.values[0]

        assert x == 0
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.gt(2)

        with pytest.raises(ValueError):
            tracker.cor_time("x1", "x2")

        with pytest.raises(ValueError):
            tracker.cor_space("x1", "x2")

        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.lt(2)


        tracker = nc.open_data(ff)
        data = nc.open_data(ff)
        tracker.subset(time = 0)
        tracker.gt(data)

        x = tracker.to_dataframe().sst.values[0]

        assert x == 0
        n = len(nc.session_files())
        assert n == 1


        tracker = nc.open_data(ff)
        data = nc.open_data(ff)
        tracker.subset(time = 0)
        tracker.lt(data)

        x = tracker.to_dataframe().sst.values[0]

        assert x == 0
        n = len(nc.session_files())
        assert n == 1







