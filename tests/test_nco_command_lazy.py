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
        data.merge("time")
        data.tmean()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncra -y mean", ensemble=False)

        data.merge("time")
        data.tmean()
        data.spatial_mean()

        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        tracker = nc.open_data("data/2003.nc")
        with pytest.raises(ValueError):
            tracker.nco_command()
        with pytest.raises(TypeError):
            tracker.nco_command(1)


        nc.options(cores = 2)
        ds = nc.open_data("data/woa*.nc")
        ds.nco_command("ncks -v t_an")
        assert ds.variables == ["t_an"]

        nc.options(cores = 1)

