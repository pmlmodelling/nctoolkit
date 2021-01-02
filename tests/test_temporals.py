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
        tracker.tmean(["month"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual mean

        tracker = nc.open_data(ff)
        tracker.tmean(["year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["day"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["season"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_mean_climatology()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual seasonal mean

        tracker = nc.open_data(ff)
        tracker.tmean(["season", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]


        # daily mean

        tracker = nc.open_data(ff)
        tracker.tmean(["day", "month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly mean

        tracker = nc.open_data(ff)
        tracker.tmean(["month", "year"])
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
        tracker.tmax(["month"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual max

        tracker = nc.open_data(ff)
        tracker.tmax(["year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_max()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["day"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["season"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_max_climatology()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily max

        tracker = nc.open_data(ff)
        tracker.tmax(["day", "month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_max()
        tracker.spatial_max()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly max

        tracker = nc.open_data(ff)
        tracker.tmax(["month", "year"])
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
        tracker.tmin(["month"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual min

        tracker = nc.open_data(ff)
        tracker.tmin(["year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_min()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["day"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["season"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_min_climatology()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily min

        tracker = nc.open_data(ff)
        tracker.tmin(["day", "month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_min()
        tracker.spatial_min()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly min

        tracker = nc.open_data(ff)
        tracker.tmin(["month", "year"])
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
        tracker.trange(["month"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        # annual range

        tracker = nc.open_data(ff)
        tracker.trange(["year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.annual_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["day"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # seasonal range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["season"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.seasonal_range_climatology()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y




        # daily range

        tracker = nc.open_data(ff)
        tracker.trange(["day", "month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.daily_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y



        # monthly range

        tracker = nc.open_data(ff)
        tracker.trange(["month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.monthly_range()
        tracker.spatial_range()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y


