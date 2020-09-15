import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestMask:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_mask(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lon=[-390, 100])
        n = len(nc.session_files())
        assert n == 0

    def test_mask1(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lat=[-390, 100])
        n = len(nc.session_files())
        assert n == 0

    def test_mask2(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lat=[-390, 100, 1])
        n = len(nc.session_files())
        assert n == 0

    def test_mask3(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lat=[0, -10])
        n = len(nc.session_files())
        assert n == 0

    def test_mask4(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lon=[0, -10])
        n = len(nc.session_files())
        assert n == 0

    def test_mask5(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mask_box(lon=[-390, 100, 1])
        n = len(nc.session_files())
        assert n == 0

    def test_mask6(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lon=1)
        n = len(nc.session_files())
        assert n == 0

    def test_mask7(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lat=1)
        n = len(nc.session_files())
        assert n == 0

    def test_mask8(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lat="1")
        n = len(nc.session_files())
        assert n == 0

    def test_mask9(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lat="2")
        n = len(nc.session_files())
        assert n == 0

    def test_mask10(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lat=["a", 1])
        n = len(nc.session_files())
        assert n == 0

    def test_mask11(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lat=[2, "b"])
        n = len(nc.session_files())
        assert n == 0

    def test_mask12(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lon=["a", 1])
        n = len(nc.session_files())
        assert n == 0

    def test_mask13(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mask_box(lon=[2, "b"])
        n = len(nc.session_files())
        assert n == 0

    def test_mask14(self):
        tracker = nc.open_data(ff)
        tracker.clip(lat=[0, 90], nco=False)
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff)
        tracker.mask_box(lat=[0, 90])
        tracker.select_timesteps(0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1
