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

    def test_xarray3(self):
        tracker = nc.open_data(ff)
        tracker.select_timesteps([0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]

        assert x == 1970

        tracker = nc.open_data(ff)
        tracker.select_timesteps([0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
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



