import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"



class TestCrop:
    def test_crop_this(self):
        tracker = nc.open_data(ff, checks = False)
        ds = nc.open_data(ff, checks = False)
        ds.subset(lon = [0, 90])
        assert ds.history[0] == 'cdo -L -sellonlatbox,0,90,-90,90'
        ds = nc.open_data(ff, checks = False)
        ds.subset(lat = [0, 90])
        assert ds.history[0] == 'cdo -L -sellonlatbox,-180,180,0,90'

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.crop(lon=[-390, 100])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.crop(lat=[-390, 100])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.crop(lat=[-390, 100, 1])

        tracker = nc.open_data(ff, checks = False)

        with pytest.raises(ValueError):
            tracker.crop(lat=[0, -10])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.crop(lon=[0, -10])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.crop(lon=[-390, 100, 1])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lon=1)

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lat=1)

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lat="1")

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lat="2")

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lat=["a", 1])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lat=[2, "b"])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lon=["a", 1])

        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.crop(lon=[2, "b"])

        tracker = nc.open_data(ff1)
        tracker.crop(lat=[0, 90], nco=True, nco_vars = "t_an")
        assert tracker.variables == ["t_an"]




        tracker = nc.open_data(ff, checks = False)
        tracker.crop(lat=[0, 90], nco=True)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff, checks = False)
        tracker.crop(lat=[0, 90], nco=False)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert np.round(x, 7) == np.round(y, 7)

        tracker = nc.open_data(ff, checks = False)
        tracker.crop(lon=[0, 90], nco=True)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff, checks = False)
        tracker.crop(lon=[0, 90], nco=False)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y

        tracker = nc.open_data(ff, checks = False)
        tracker.crop(lon=[0, 90], nco=True)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=[0, 1])
        tracker.split("yearmonth")
        tracker.crop(lon=[0, 90], nco=False)
        tracker.merge("time")
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
