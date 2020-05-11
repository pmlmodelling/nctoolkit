import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


class TestSeasclim(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_mean_climatology()
        tracker.select_season("DJF")
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.mean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]


        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_max_climatology()
        tracker.select_season("DJF")
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.max()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]


        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_min_climatology()
        tracker.select_season("DJF")
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.min()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]


        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_range_climatology()
        tracker.select_season("DJF")
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.range()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]


        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

