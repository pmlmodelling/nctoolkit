import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestTolonat(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_latlon1(self):
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
        tracker.to_latlon(lon = [0.5,89.5], lat = [0.5,89.5], res = [1,1], method = "nn")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_latlon2(self):
        tracker = nc.open_data(ff)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = 1, lat = 2, res = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = 1, lat = 2)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lat = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = 1, lat = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2])


        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2],  res = [1, -1])


        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2])


        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1], lat = [1,2], res = [1, -1])


        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,1], lat = [1], res = [1, -1])

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2], res = [1, -1])

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2], res = [1, 0])

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2], res = [0, 1])

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2], res = [1, "test"])

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1,2], lat = [1,2], res = ["test", 1])

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1, "x"], lat = [1,2], res = 1)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = ["x", 1], lat = [1, "y"], res = 1)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [2, "x"], lat = [1, "y"], res = 1)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1, 1], lat = ["y", 1], res = 1)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1, 1], lat = [1, "y"], res = 1)

        with self.assertRaises(TypeError) as context:
            tracker.to_latlon(lon = [1, 2], lat = [1, 2], res = "test")

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1, 2,3], lat = [1, 2])

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1, 2], lat = [1, 2,3], res = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [2, 1], lat = [1, 2], res = 1)

        with self.assertRaises(ValueError) as context:
            tracker.to_latlon(lon = [1, 2], lat = [2, 1], res = 1)

    def test_latlon4(self):
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
        tracker.to_latlon(lon = [0.5,89.5], lat = [0.5,89.5], res = 1, method = "nn")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

