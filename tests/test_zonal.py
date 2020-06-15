import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestClip(unittest.TestCase):

    def test_zonal1(self):
        tracker = nc.open_data(ff)
        n = len(nc.session_files())
        assert n == 0

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.zonal_mean()
        data.spatial_mean()
        assert data.to_dataframe().sst[0].values[0].astype("float") == 17.550573348999023

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.zonal_min()
        data.spatial_mean()
        assert data.to_dataframe().sst[0].values[0].astype("float") == 13.19449520111084

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.zonal_max()
        data.spatial_mean()
        assert data.to_dataframe().sst[0].values[0].astype("float") == 20.55069923400879

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.mean()
        data.zonal_range()
        data.spatial_mean()
        assert data.to_dataframe().sst[0].values[0].astype("float") == 7.356204986572266

if __name__ == '__main__':
    unittest.main()

