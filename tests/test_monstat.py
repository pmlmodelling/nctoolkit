import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/2003.nc"

class TestSelect(unittest.TestCase):

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_mean()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")


        self.assertEqual(x,  286.9499816894531)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_min()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")


        self.assertEqual(x, 286.19000244140625)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_max()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")


        self.assertEqual(x, 287.67999267578125)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.monthly_range()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().analysed_sst.values[0].astype("float")


        self.assertEqual(x, 1.480010986328125)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

