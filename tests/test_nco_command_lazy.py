import nctoolkit as nc
import platform

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestNCO:
    def test_empty_nco(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean_nco(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"), checks = False)
        data.ensemble_mean(nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"), checks=False)
        data.nco_command("ncea -y mean", ensemble=True)
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

    def test_mean2_nco(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"), checks=False)
        data.tmean()
        data.merge("time")
        data.tmean()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"), checks= False)
        data.nco_command("ncra -y mean", ensemble=False)

        data.merge("time")
        data.tmean()
        data.spatial_mean()

        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        tracker = nc.open_data("data/2003.nc", checks=False)
        with pytest.raises(ValueError):
            tracker.nco_command()
        with pytest.raises(ValueError):
            tracker.nco_command("ncblah -y mean", ensemble=False)
        with pytest.raises(TypeError):
            tracker.nco_command(1)

        ff = "data/sst.mon.mean.nc"

        # Run this check below on linux
        if platform.system() == "Linux":
            nc.options(cores = 2)
            ds = nc.open_data(ff, checks=False)
            ds.subset(time = 0)
            ds.assign(t_k = lambda x: x.sst+273.15)
            # select t_k using NCO
            ds.nco_command("ncks -v t_k", ensemble=False)
            assert ds.variables[0] == "t_k"
            nc.options(cores = 1)






