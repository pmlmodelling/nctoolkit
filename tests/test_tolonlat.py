import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_lonlat1(self):
        print(nc.session_files())
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.to_lonlat(lon = [0.5,89.5], lat = [0.5,89.5], res = [1,1], method = "nn")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

