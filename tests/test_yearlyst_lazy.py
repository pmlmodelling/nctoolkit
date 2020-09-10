import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestYearlyst(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

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



    def test_annualsum(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.sum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.annual_sum()
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

