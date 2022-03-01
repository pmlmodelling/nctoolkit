import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestTemporals:
    def test_temporals_mean(self):
        version = nc.utils.cdo_version()
        n = len(nc.session_files())
        assert n == 0

        if nc.utils.version_below(version, "1.9.8") == False:
            ds = nc.open_data(ff)
            ds.na_count()
            ds.spatial_sum()
            ds.to_dataframe()
            assert ds.to_dataframe().sst.values[0] == 7560360.0 

            ds = nc.open_data(ff)
            ds.na_frac()
            ds.spatial_sum()
            ds.to_dataframe()
            assert ds.to_dataframe().sst.values[0] == 21001.0 

            del ds

        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["month"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.tvar()
        ds.spatial_sum()
        ds.to_dataframe()
        assert ds.to_dataframe().sst.values[0] == 133869.140625 

        del ds

        assert x == 18.002004623413086

        tracker = nc.open_data(ff)
        tracker.tmean(["month", "day"])
        tracker.spatial_mean()
        y = float(tracker.to_dataframe().sst.values[0])
        assert y == x 

        tracker = nc.open_data(ff)
        tracker.tpercentile(over = ["month"], p =0.05)
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        tracker = nc.open_data(ff)
        tracker.tpercentile( over = ["month", "day"], p = 0.05)
        tracker.spatial_mean()
        y = float(tracker.to_dataframe().sst.values[0])
        assert y == x 

        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.tmean()

        with pytest.raises(ValueError):
            tracker.tpercentile(p = 0.05)

        # annual mean

        tracker = nc.open_data(ff)
        tracker.tmean(["year"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x == 17.92256736755371




        # daily mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["day"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x == 18.002004623413086




        # seasonal mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["season"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])

        assert x == 17.9996280670166


        # annual seasonal mean

        tracker = nc.open_data(ff)
        tracker.tmean(["season", "year"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x == 18.0740909576416

        # daily mean

        tracker = nc.open_data(ff)
        tracker.tmean(["day", "month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 18.02419662475586



        # monthly mean

        tracker = nc.open_data(ff)
        tracker.tmean(["month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 18.02419662475586









    def test_temporals_max(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["month"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 30.970001220703125


        # annual max

        tracker = nc.open_data(ff)
        tracker.tmax(["year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 33.48500061035156


        # daily max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["day"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 30.970001220703125




        # seasonal max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["season"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 31.173002243041992




        # daily max

        tracker = nc.open_data(ff)
        tracker.tmax(["day", "month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 30.430002212524414



        # monthly max

        tracker = nc.open_data(ff)
        tracker.tmax(["month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 30.430002212524414









    def test_temporals_min(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["month"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8540000915527344


        # annual min

        tracker = nc.open_data(ff)
        tracker.tmin(["year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8540000915527344




        # daily min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["day"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8540000915527344


        # seasonal min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["season"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8610000610351562




        # daily min

        tracker = nc.open_data(ff)
        tracker.tmin(["day", "month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8530000448226929



        # monthly min

        tracker = nc.open_data(ff)
        tracker.tmin(["month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8530000448226929



    def test_temporals_range(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.trange(["month"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 7.600000381469727


        # annual range

        tracker = nc.open_data(ff)
        tracker.trange(["year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 24.88800048828125


        # daily range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["day"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 7.600000381469727




        # seasonal range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["season"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 10.569000244140625




        # daily range

        tracker = nc.open_data(ff)
        tracker.trange(["day", "month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 0



        # monthly range

        tracker = nc.open_data(ff)
        tracker.trange(["month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 0


