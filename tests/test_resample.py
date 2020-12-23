import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"



class TestResample:
    def test_resample(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.resample_grid(factor = 0)
        with pytest.raises(TypeError):
            tracker.resample_grid(factor = "x")

        with pytest.raises(ValueError):
            tracker.resample_grid()

        x = len(tracker.to_xarray().lon.values)

        tracker.resample_grid(factor = 2)
        y = len(tracker.to_xarray().lon.values)

        assert x  == y * 2



        del tracker
        n = len(nc.session_files())
        assert n == 0

