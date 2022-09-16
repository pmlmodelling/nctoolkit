import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestCompare:
    def test_compare(self):

        tracker = nc.open_data(ff)
        tracker1 = nc.open_data("data/ensemble/*.nc")
        with pytest.raises(ValueError):
            tracker.gt(tracker1)

        with pytest.raises(ValueError):
            tracker.lt(tracker1)

        tracker = nc.open_data(ff)

        tracker.subset(time = 0)
        tracker.gt(ff)

        x = tracker.to_dataframe().sst.values[0]
        none = []

        assert x == 0
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.gt(2)

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)
            tracker.gt(none)

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)
            tracker.lt(none)

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)
            tracker.lt("x")

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)
            tracker.gt("x")


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

        tracker = nc.open_data(ff)
        data = nc.open_data(ff)
        tracker.subset(time = 0)
        tracker.gt(data[0])

        x = tracker.to_dataframe().sst.values[0]

        assert x == 0



        tracker = nc.open_data(ff)
        data = nc.open_data(ff)
        tracker.subset(time = 0)
        tracker.lt(data)

        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        data = nc.open_data(ff)
        tracker.subset(time = 0)
        tracker.lt(data[0])

        x = tracker.to_dataframe().sst.values[0]


        assert x == 0
        n = len(nc.session_files())
        assert n == 1







