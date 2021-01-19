import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestCor:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_cor(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.mutate({"tos": "sst+273.15"})
        tracker.cor_space(var1="tos", var2="sst")
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor_list(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.mutate({"tos": "sst+273.15"})
        tracker.cor_space(var1="tos", var2="sst")
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor1(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos": "sst+273.15"})
        tracker.cor_time(var1="tos", var2="sst")
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=range(1990, 2000))
        tracker.mutate({"tos": "sst+273.15"})
        tracker.split("year")
        tracker.cor_time(var1="tos", var2="sst")
        assert 10 == len(tracker.current)
        tracker.merge_time()
        assert 10 == len(tracker.years)
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.cor_space()
        n = len(nc.session_files())
        assert n == 0

        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.mutate({"tos": "sst+273.15"})
        with pytest.raises(ValueError):
            tracker.cor_space(var1="x", var2="y")
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.mutate({"tos": "sst+273.15"})
        with pytest.raises(ValueError):
            tracker.cor_space(var1="tos", var2="y")
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.cor_space(var1=1, var2="y")

        with pytest.raises(TypeError):
            tracker.cor_space(var1="x", var2=1)
