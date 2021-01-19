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

    def test_compare_all(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all("<=0")
        tracker.run()
        tracker.spatial_sum()
        n = len(nc.session_files())
        assert n == 1

        x = tracker.to_dataframe().sst.values[0].astype("int")

    def test_compare_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.compare_all("==")
        with pytest.raises(ValueError):
            tracker.compare_all("<=")
        with pytest.raises(ValueError):
            tracker.compare_all(">=")

        with pytest.raises(ValueError):
            tracker.compare_all(">")
        with pytest.raises(ValueError):
            tracker.compare_all("<")
        with pytest.raises(ValueError):
            tracker.compare_all("")
        with pytest.raises(ValueError):
            tracker.compare_all("!=")

        with pytest.raises(ValueError):
            tracker.compare_all()

        with pytest.raises(TypeError):
            tracker.compare_all(1)

        n = len(nc.session_files())

        assert n == 0

    def test_compare_all1(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all("<0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 9356

        n = len(nc.session_files())
        assert n == 1

    def test_compare_all2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all(">0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")
        assert x == 34441

        n = len(nc.session_files())
        assert n == 1

    def test_compare_all3(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all("==0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 2
        n = len(nc.session_files())
        assert n == 1

    def test_compare_all4(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all("!=0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 43797
        n = len(nc.session_files())
        assert n == 1

    def test_compare_all5(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.compare_all(">=0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 34443
        n = len(nc.session_files())
        assert n == 1
