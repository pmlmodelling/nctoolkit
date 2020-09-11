import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestEnsemble:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_ens_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 17.996946334838867

        n = len(nc.session_files())
        assert n == 1

    def test_ens_max(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max(nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 19.205900192260742
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max(nco=True, ignore_time=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.max()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max(nco=False, ignore_time=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max(nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 19.205900192260742
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max(nco=False)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 19.205900192260742

    def test_ens_min(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_min()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 16.958738327026367
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_min(nco=True)
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

    def test_ignore_time(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(ignore_time=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data("data/sst.mon.mean.nc")
        data.min()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data("data/sst.mon.mean.nc")
        data.split("year")
        data.ensemble_min(ignore_time=True)
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

    def test_ignore_time_2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(ignore_time=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        n = len(nc.session_files())

        data = nc.open_data("data/sst.mon.mean.nc")
        data.ensemble_mean(ignore_time=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        data = nc.open_data("data/sst.mon.mean.nc")
        data.ensemble_mean(ignore_time=True, nco=True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        assert x == y

        assert n == 1

    def test_ens_range(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_range()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 2.2471628189086914
        n = len(nc.session_files())
        assert n == 1

    def test_ens_percent(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_percentile(40)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 17.851171493530273
        n = len(nc.session_files())
        assert n == 1

    def test_ens_percent_error(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with pytest.raises(TypeError):
            data.ensemble_percentile("a")
        n = len(nc.session_files())
        assert n == 0

    def test_ens_percent_error1(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with pytest.raises(ValueError):
            data.ensemble_percentile(129)
        n = len(nc.session_files())
        assert n == 0

    def test_ens_warn(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_percentile(40)

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_max()

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_min()

        n = len(nc.session_files())
        assert n == 0

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_mean()
        data.release()
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_range()
        data.run()
        n = len(nc.session_files())
        assert n == 1

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with pytest.warns(UserWarning):
            data.ensemble_range()
        data.run()
        n = len(nc.session_files())
        assert n == 1

    def test_ens_pnone(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with pytest.raises(ValueError):
            data.ensemble_percentile()
