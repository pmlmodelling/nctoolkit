import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestPhenol:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_clim1(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="peak")
        data.spatial_mean()

        x = data.to_dataframe().peak.values[0].astype("float")

        assert x == 4.852420330047607
        n = len(nc.session_files())

        assert n == 1

    def test_start_mid(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="middle")
        data.spatial_mean()

        x = data.to_dataframe().middle.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start", p=50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        assert x == y

    def test_start_end(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="end", p=50)
        data.spatial_mean()

        x = data.to_dataframe().end.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start", p=50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        assert x == y

    def test_error(self):
        data = nc.open_data(ff)

        with pytest.raises(ValueError):
            data.phenology("sst", metric="this")

        with pytest.raises(ValueError):
            data.phenology("sst", metric="peak")
        with pytest.raises(ValueError):
            data.phenology("sst", metric="middle")

        n = len(nc.session_files())
        assert n == 0

        with pytest.raises(TypeError):
            data.phenology("sst", metric="start", p="2")

    def test_typeerror(self):
        data = nc.open_data(ff)
        with pytest.raises(TypeError):
            data.phenology(var=1, metric="peak")
        n = len(nc.session_files())
        assert n == 0

    def test_nometricerror(self):
        data = nc.open_data(ff)
        with pytest.raises(ValueError):
            data.phenology("sst")

        with pytest.raises(ValueError):
            data.phenology(metric="peak")

    def test_defaults(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="end")
        data.spatial_mean()

        x = data.to_dataframe().end.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start", p=75)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        assert x == y

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start")
        data.spatial_mean()

        x = data.to_dataframe().start.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start", p=25)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        assert x == y

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="middle")
        data.spatial_mean()

        x = data.to_dataframe().middle.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric="start", p=50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        assert x == y
