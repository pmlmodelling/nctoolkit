import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"

class TestReset:
    def test_reset(self):
        ds = nc.open_data(ff, checks = False)
        x = ds.current
        ds.tmean()
        ds.run()
        y = ds.current
        ds.reset()
        z = ds.current
        assert z != y
        assert x  == z

        ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1981-2010.nc", checks = False)
        x = ds.current
        ds.tmean()
        ds.reset()
        z = ds.current
        assert x  == z
