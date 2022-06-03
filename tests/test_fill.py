import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestFill:

    def test_fill(self):
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds.cdo_command("setmisstonn")
        x = ds.to_dataframe().sst.values[0].astype("float")

        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds.fill_na()
        y = ds.to_dataframe().sst.values[0].astype("float")



        assert x == y
