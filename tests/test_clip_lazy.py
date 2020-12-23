import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"



class TestCrop:
    def test_crop(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.crop(lon=[-390, 100])
        n = len(nc.session_files())
        assert n == 0

    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_crop1(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.crop(lat=[-390, 100])
        n = len(nc.session_files())
        assert n == 0

    def test_crop2(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.crop(lat=[-390, 100, 1])
        n = len(nc.session_files())
        assert n == 0

    def test_crop3(self):
        tracker = nc.open_data(ff)

        with pytest.raises(ValueError):
            tracker.crop(lat=[0, -10])
        n = len(nc.session_files())
        assert n == 0

    def test_crop4(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.crop(lon=[0, -10])
        n = len(nc.session_files())
        assert n == 0

    def test_cropr5(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.crop(lon=[-390, 100, 1])
        n = len(nc.session_files())
        assert n == 0

    def test_crop6(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lon=1)
        n = len(nc.session_files())
        assert n == 0

    def test_crop7(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lat=1)
        n = len(nc.session_files())
        assert n == 0

    def test_crop8(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lat="1")
        n = len(nc.session_files())
        assert n == 0

    def test_crop9(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lat="2")
        n = len(nc.session_files())
        assert n == 0

    def test_crop10(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lat=["a", 1])
        n = len(nc.session_files())
        assert n == 0

    def test_crop11(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lat=[2, "b"])
        n = len(nc.session_files())
        assert n == 0

    def test_crop12(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lon=["a", 1])
        n = len(nc.session_files())
        assert n == 0

    def test_crop13(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.crop(lon=[2, "b"])
        n = len(nc.session_files())
        assert n == 0

    def test_nco_vars(self):
        tracker = nc.open_data(ff1)
        tracker.crop(lat=[0, 90], nco=True, nco_vars = "t_an")
        assert tracker.variables == ["t_an"]




    def test_nco(self):
        tracker = nc.open_data(ff)
        tracker.crop(lat=[0, 90], nco=True)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff)
        tracker.crop(lat=[0, 90], nco=False)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_nco2(self):
        tracker = nc.open_data(ff)
        tracker.crop(lon=[0, 90], nco=True)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff)
        tracker.crop(lon=[0, 90], nco=False)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_nco3(self):
        tracker = nc.open_data(ff)
        tracker.crop(lon=[0, 90], nco=True)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff)
        tracker.select_timesteps([0, 1])
        tracker.split("yearmonth")
        tracker.crop(lon=[0, 90], nco=False)
        tracker.merge_time()
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1
