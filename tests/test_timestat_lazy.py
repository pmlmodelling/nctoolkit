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
        tracker = nc.open_data(ff)
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
        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        tracker.tpercentile(60)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select(years=[1990, 1991])
        tracker.split("year")
        tracker.tpercentile(60)
        tracker.select(years=1990)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y


        tracker = nc.open_data(ff)
        tracker.tpercentile(50)
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff)
        tracker.tmedian()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y




    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=0)

        tracker1 = nc.open_data(ff)
        tracker1.select(timesteps=1)

        tracker2 = nc.open_data(ff)
        tracker2.select(timesteps=[0, 1])
        tracker2.tsum()
        tracker2.spatial_sum()
        x = tracker2.to_dataframe().sst.values[0]
        tracker1.add(tracker)
        tracker1.spatial_sum()
        y = tracker1.to_dataframe().sst.values[0]

        assert x == y

    def test_variance(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=range(0, 12))

        tracker.tvar()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 3.3688883781433105

    def test_cumsum(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=range(0, 12))

        tracker.tcumsum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 12.964875221252441
