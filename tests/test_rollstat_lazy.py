import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_mean(self):
        tracker = nc.open_data(ff)
        tracker.rolling_mean(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,  18.092084884643555 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        tracker = nc.open_data(ff)
        tracker.rolling_max(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x,20.390228271484375)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        tracker = nc.open_data(ff)
        tracker.rolling_min(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 16.16268539428711)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        tracker = nc.open_data(ff)
        tracker.rolling_range(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 4.227542877197266)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 180.9208526611328)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_float(self):
        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10)
        tracker.select_years(2000)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")


        tracker = nc.open_data(ff)
        tracker.rolling_sum(window = 10.0)
        tracker.select_years(2000)
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
        n = len(nc.session_files())
        self.assertEqual(n, 0)


if __name__ == '__main__':
    unittest.main()
