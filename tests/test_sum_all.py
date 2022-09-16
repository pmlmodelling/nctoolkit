import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestSumall:
    def test_sumall(self):
        ds = nc.open_data(["data/2003.nc", "data/2004.nc"])
        ds.subset(time = 0)
        ds.assign(tos1 = lambda x: -x.analysed_sst)
        ds.sum_all()
        ds.merge("time")
        assert ds.to_dataframe().total.abs().max() < 1e-4

        ds = nc.open_data(["data/2003.nc", "data/2004.nc"])
        ds.subset(time = 0)
        ds.assign(total = lambda x: -x.analysed_sst)
        ds.sum_all(drop = False)
        ds.merge("time")
        assert ds.to_dataframe().total0.abs().max() < 1e-4

        ds = nc.open_data(["data/2003.nc", "data/2004.nc"])
        ds.subset(time = 0)
        ds.assign(total = lambda x: -x.analysed_sst)
        ds.rename({"analysed_sst":"total0"})
        ds.sum_all(drop = False)
        ds.merge("time")
        assert ds.to_dataframe().total1.abs().max() < 1e-4

        with pytest.raises(TypeError):
            ds = nc.open_data(["data/2003.nc",ff])
            ds.sum_all()


        ds = nc.open_data(["data/2003.nc", "data/2004.nc"])
        ds.subset(time = 0)
        ds.assign(tos1 = lambda x: -x.analysed_sst)
        ds.sum_all(drop = False)
        ds.merge("time")
        assert ds.to_dataframe().total.abs().max() < 1e-4
