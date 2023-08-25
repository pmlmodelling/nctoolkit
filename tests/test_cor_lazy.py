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
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=1)
        tracker.assign(tos =  lambda x: x.sst+273.15)
        tracker.cor_space(var1="tos", var2="sst")
        x = tracker.to_dataframe().cor.values[0]

        ## test valuerror  raised

        with pytest.raises(ValueError):
            ds1 = nc.open_data(ff, checks = False)
            ds1.subset(time = 0)
            ds2 = nc.open_data(ff, checks = False)
            ds2.subset(time = 0)
            ds2.set_precision("F64")
            ds2.rename({"sst": "tos"})
            ds1.append(ds2)
            ds1.merge("variables)")
            ds1.cor_space(var1="tos", var2="sst")

            del ds1
            del ds2

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 3




    def test_cor_list(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=1)
        tracker.assign(tos = lambda x: x.sst+273.15)
        tracker.cor_space(var1="tos", var2="sst")
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor1(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.assign(tos = lambda x: x.sst+273.15)
        tracker.cor_time(var1="tos", var2="sst")
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=range(1990, 2000))
        tracker.assign(tos = lambda x: x.sst+273.15)
        tracker.split("year")
        tracker.cor_time(var1="tos", var2="sst")
        assert 10 == len(tracker.current)
        tracker.merge("time")
        assert 10 == len(tracker.years)
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        assert x == 1.0
        n = len(nc.session_files())
        assert n == 1

    def test_cor_error(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.cor_space()
        n = len(nc.session_files())
        assert n == 0

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=1)
        tracker.assign(tos = lambda x: x.sst+273.15)
        with pytest.raises(ValueError):
            tracker.cor_space(var1="x", var2="y")
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=1)
        tracker.assign(tos = lambda x: x.sst+273.15)
        with pytest.raises(ValueError):
            tracker.cor_space(var1="tos", var2="y")
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.cor_space(var1=1, var2="y")

        with pytest.raises(TypeError):
            tracker.cor_space(var1="x", var2=1)
