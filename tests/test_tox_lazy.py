import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"
ff2 = "data/woa18_decav_t02_01.nc"


class TestToxar:
    def test_xarray2(self):
        tracker = nc.open_data(ff1)
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
        assert x == 1986
        ds = nc.open_data("data/sst.mon.mean.nc")
        assert len(ds.to_xarray(time = range(0, 3)).time.values) == 3

        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.subset(time = range(0, 3))
        ds.split("month")
        assert len(ds.to_xarray().time.values) == 3

        ds = nc.open_data("data/woa18_decav_t01_01.nc")
        x = ds.to_xarray().time.values[0]
        assert str(x) == '1986-01-16T12:00:00.000000000'


    def test_xarray3(self):
        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]

        assert x == 1970

        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
        y = tracker.to_dataframe(decode_times=True).reset_index().time.dt.year.values[0]
        assert x == y


        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0])
        tracker.spatial_mean()
        x = tracker.to_dataframe(decode_times=True).reset_index().time.dt.year.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0])
        ds = tracker.to_xarray()
        tracker = nc.from_xarray(ds)
        tracker.spatial_mean()
        y = tracker.to_dataframe(decode_times=True).reset_index().time.dt.year.values[0]

        assert x == y



        tracker = nc.open_data(ff)
        ds1 = tracker.to_xarray()
        ds2 = xr.open_dataset(ff)
        assert ds1.equals(ds2)

        ds1 = tracker.to_xarray(decode_times = False)
        ds2 = xr.open_dataset(ff, decode_times = False)
        assert ds1.equals(ds2)




        tracker = nc.open_data([ff1,ff2])
        ds1 = tracker.to_xarray(decode_times = False)
        ds2 = xr.open_mfdataset([ff1, ff2], decode_times = False)
        assert ds1.equals(ds2)

        with pytest.raises(ValueError):
            ds1 = tracker.to_xarray()



