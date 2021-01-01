import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestTemporals:
    def test_temporals_mean(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.mean(["month"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual mean

        tracker = nc.open_data(ff)
        tracker.mean(["year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily mean climatology

        tracker = nc.open_data(ff)
        tracker.mean(["day"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal mean climatology

        tracker = nc.open_data(ff)
        tracker.mean(["season"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual seasonal mean

        tracker = nc.open_data(ff)
        tracker.mean(["season", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]


        # daily mean

        tracker = nc.open_data(ff)
        tracker.mean(["day", "month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly mean

        tracker = nc.open_data(ff)
        tracker.mean(["month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y









    def test_temporals_max(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.max(["month"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual max

        tracker = nc.open_data(ff)
        tracker.max(["year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_max()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily max climatology

        tracker = nc.open_data(ff)
        tracker.max(["day"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal max climatology

        tracker = nc.open_data(ff)
        tracker.max(["season"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily max

        tracker = nc.open_data(ff)
        tracker.max(["day", "month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_max()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly max

        tracker = nc.open_data(ff)
        tracker.max(["month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_max()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y









    def test_temporals_min(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.min(["month"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual min

        tracker = nc.open_data(ff)
        tracker.min(["year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_min()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily min climatology

        tracker = nc.open_data(ff)
        tracker.min(["day"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal min climatology

        tracker = nc.open_data(ff)
        tracker.min(["season"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily min

        tracker = nc.open_data(ff)
        tracker.min(["day", "month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_min()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly min

        tracker = nc.open_data(ff)
        tracker.min(["month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_min()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



    def test_temporals_range(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.range(["month"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual range

        tracker = nc.open_data(ff)
        tracker.range(["year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily range climatology

        tracker = nc.open_data(ff)
        tracker.range(["day"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal range climatology

        tracker = nc.open_data(ff)
        tracker.range(["season"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily range

        tracker = nc.open_data(ff)
        tracker.range(["day", "month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly range

        tracker = nc.open_data(ff)
        tracker.range(["month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


