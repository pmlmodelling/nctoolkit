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

    def test_compare_all(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all("<=0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 9512)

    def test_compare_all1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all("<0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 9509)


    def test_compare_all2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all(">0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 34287)

    def test_compare_all3(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all("==0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 3)

    def test_compare_all4(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all("!=0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 43796)



    def test_compare_all5(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.compare_all(">=0")
        tracker.release()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")


        self.assertEqual(x, 34290)


if __name__ == '__main__':
    unittest.main()

