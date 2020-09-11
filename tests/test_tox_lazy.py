import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"


class TestToxar:
    def test_xarray2(self):
        tracker = nc.open_data(ff1)
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
        assert x == 1986

    def test_xarray3(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]

        assert x == 1970

    def test_df(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0])
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
        y = tracker.to_dataframe(decode_times=True).reset_index().time.dt.year.values[0]
        assert x == y
