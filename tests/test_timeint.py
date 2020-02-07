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

    def test_timeint(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "2000/01/01", end = "2000/31/01", resolution = "daily")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 366)

    def test_timeint1(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "2001/01/01", end = "2001/31/01", resolution = "weekly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 53)

    def test_timeint2(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "2000/01/01", end = "2000/31/01", resolution = "monthly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 12)


    def test_timeint3(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "2000/01/01", end = "2003/01/01", resolution = "yearly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 4)



if __name__ == '__main__':
    unittest.main()

