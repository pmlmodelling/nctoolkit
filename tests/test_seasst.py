import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(2000)
        tracker.seasonal_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -1.6850000619888306)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(2000)
        tracker.seasonal_min()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -1.6920000314712524)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(2000)
        tracker.seasonal_max()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -1.6780000925064087 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(2000)
        tracker.seasonal_range()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 0.01399993896484375 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

