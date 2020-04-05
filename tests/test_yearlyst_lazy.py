import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):


    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.annual_mean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.min()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.annual_min()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.max()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.annual_max()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.range()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.annual_range()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)



if __name__ == '__main__':
    unittest.main()

