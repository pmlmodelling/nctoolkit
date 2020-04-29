import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestRollstat(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.rolling_mean(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,  18.077280044555664)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.rolling_max(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 20.302736282348633)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.rolling_min(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,  16.211519241333008)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.rolling_range(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 4.091217517852783)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,  180.77279663085938)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_float(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")


        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10)
        tracker.select_years(1990)
        tracker.spatial_mean()
        tracker.release()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")


        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.rolling_sum(window = "x")

        with self.assertRaises(ValueError) as context:
            tracker.rolling_sum()

        with self.assertRaises(ValueError) as context:
            tracker.rolling_sum(window = 0)

        with self.assertRaises(ValueError) as context:
            tracker.rolling_sum(window = -1)


        n = len(nc.session_files())
        self.assertEqual(n, 0)


if __name__ == '__main__':
    unittest.main()
