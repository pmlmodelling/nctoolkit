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
            tracker.percentile(p="x")

        with pytest.raises(ValueError):
            tracker.percentile()

        with pytest.raises(ValueError):
            tracker.percentile(p=120)

    def test_percentile(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.percentile(60)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years([1990, 1991])
        tracker.split("year")
        tracker.percentile(60)
        tracker.select_years(1990)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y

    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.select_timesteps(0)

        tracker1 = nc.open_data(ff)
        tracker1.select_timesteps(1)

        tracker2 = nc.open_data(ff)
        tracker2.select_timesteps([0, 1])
        tracker2.sum()
        tracker2.spatial_sum()
        x = tracker2.to_dataframe().sst.values[0]
        tracker1.add(tracker)
        tracker1.spatial_sum()
        y = tracker1.to_dataframe().sst.values[0]

        assert x == y

    def test_variance(self):
        tracker = nc.open_data(ff)
        tracker.select_timesteps(range(0, 12))

        tracker.variance()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 3.3688883781433105

    def test_cum_sum(self):
        tracker = nc.open_data(ff)
        tracker.select_timesteps(range(0, 12))

        tracker.cum_sum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 12.964875221252441
