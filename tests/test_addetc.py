import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_add(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.add(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + 1, y)

    def test_add2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + x, y)

    def test_subtract2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(1)
        new.subtract(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(y, 1)

    def test_subtract(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.subtract(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x - 1, y)

    def test_multiply(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.multiply(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(np.round(x * 10, 4).astype("float"), np.round(y, 4).astype("float"))

    def test_multiply2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.multiply(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y*2)

    def test_divide(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.divide(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(np.round(x / 10, 4), np.round(y, 4))


    def test_divide2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y/2)


if __name__ == '__main__':
    unittest.main()

