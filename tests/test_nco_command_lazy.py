import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestNCO:
    def test_empty_nco(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mean_nco(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncea -y mean", ensemble=True)
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

    def test_mean2_nco(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.tmean()
        data.merge_time()
        data.tmean()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncra -y mean", ensemble=False)

        data.merge_time()
        data.tmean()
        data.spatial_mean()

        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y
