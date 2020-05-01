import unittest
import nchack as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestCompare(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_compare_all(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all("<=0")
        tracker.release()
        tracker.spatial_sum()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

        x = tracker.to_dataframe().sst.values[0].astype("int")


    def test_compare_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.compare_all("==")
        with self.assertRaises(ValueError) as context:
            tracker.compare_all("<=")
        with self.assertRaises(ValueError) as context:
            tracker.compare_all(">=")

        with self.assertRaises(ValueError) as context:
            tracker.compare_all(">")
        with self.assertRaises(ValueError) as context:
            tracker.compare_all("<")
        with self.assertRaises(ValueError) as context:
            tracker.compare_all("")
        with self.assertRaises(ValueError) as context:
            tracker.compare_all("!=")

        with self.assertRaises(ValueError) as context:
            tracker.compare_all()

        with self.assertRaises(TypeError) as context:
            tracker.compare_all(1)

        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_compare_all1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all("<0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 9356)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_compare_all2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all(">0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")
        self.assertEqual(x, 34441)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_compare_all3(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all("==0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 2)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_compare_all4(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all("!=0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 43797)
        n = len(nc.session_files())
        self.assertEqual(n, 1)



    def test_compare_all5(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.compare_all(">=0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 34443)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

