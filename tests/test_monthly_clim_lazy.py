import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestMonthlycli:
    def test_monthlyclim(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.select_months(1)
        tracker.tmean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.monthly_mean_climatology()
        tracker.select_months(1)
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.select_months(1)
        tracker.tmin()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.monthly_min_climatology()
        tracker.select_months(1)
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.select_months(1)
        tracker.tmax()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.monthly_max_climatology()
        tracker.select_months(1)
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.select_months(1)
        tracker.trange()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1999))
        tracker.monthly_range_climatology()
        tracker.select_months(1)
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1
