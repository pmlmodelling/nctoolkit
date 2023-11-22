import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestTimestat:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_error(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.tpercentile(p="x")

        with pytest.raises(ValueError):
            tracker.tmean("x")
        with pytest.raises(ValueError):
            tracker.tmean(["month", "season"])

        with pytest.raises(ValueError):
            tracker.tpercentile(p = 50, over = ["month", "season"])

        with pytest.raises(ValueError):
            tracker.tpercentile(p = 50, over = "x")


        with pytest.raises(ValueError):
            tracker.tpercentile()

        with pytest.raises(ValueError):
            tracker.tpercentile(p=120)

    def test_percentile(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.tpercentile(60)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=[1990, 1991])
        tracker.split("year")
        tracker.tpercentile(60)
        tracker.subset(years=1990)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        tracker = nc.open_data(ff, checks = False)
        tracker.tpercentile(50)
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff, checks = False)
        tracker.tmedian()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y




    def test_sum(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=0)

        tracker1 = nc.open_data(ff, checks = False)
        tracker1.subset(timesteps=1)

        tracker2 = nc.open_data(ff, checks = False)
        tracker2.subset(timesteps=[0, 1])
        tracker2.tsum()
        tracker2.spatial_sum()
        x = tracker2.to_dataframe().sst.values[0]
        tracker1.add(tracker)
        tracker1.spatial_sum()
        y = tracker1.to_dataframe().sst.values[0]

        assert x == y

    def test_variance(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=range(0, 12))

        tracker.tvar()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x ==  9.449978828430176 

    def test_cumsum(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=range(0, 12))

        tracker.tcumsum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 9.221193313598633 
    
    def test_tstatwindow(self):
        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tmean()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))

        ds2.tmean(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # max
        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tmax()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))

        ds2.tmax(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # min
        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tmin()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))

        ds2.tmin(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # range
        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.trange()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))

        ds2.trange(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # std

        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tstdev()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))
        
        ds2.tstdev(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # var
        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tvar()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))

        ds2.tvar(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()

        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        # sum

        ds1 = nc.open_data("data/2003.nc")
        ds1.subset(time = range(0, 5))
        ds1.tsum()
        ds1.run()
        ds2 = nc.open_data("data/2003.nc")
        ds2.subset(time = range(0, 5))
        
        ds2.tsum(window = 5)
        ds2.run()
        ds1 - ds2
        ds1.spatial_mean()
        assert ds1.to_dataframe().analysed_sst.mean() == 0.0

        ds1 = nc.open_data("data/2003.nc")
        ds1.tmean(window = 5)
        assert (ds1.times[5] - ds1.times[0]).days == 25

