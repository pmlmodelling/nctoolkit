import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.ltm.1981-2010.nc"


class TestApi2(unittest.TestCase):

    def test_url(self):
        tracker = nc.open_data(ff)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data("ftp://ftp.cdc.noaa.gov/Datasets/COBE/sst.mon.ltm.1981-2010.nc")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        print(x)
        print(y)
        assert x == y


if __name__ == '__main__':
    unittest.main()

