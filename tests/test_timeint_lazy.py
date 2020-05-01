import unittest
import nchack as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestTimeint(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_timeint(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "1990/01/01", end = "1990/31/01", resolution = "daily")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 365)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timeint1(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "1991/01/01", end = "1991/31/01", resolution = "weekly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 53)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timeint2(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "1990/01/01", end = "1990/31/01", resolution = "monthly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 12)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_timeint3(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "1990/01/01", end = "1993/01/01", resolution = "yearly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 4)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timeint4(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start = "1990/01/01",  resolution = "yearly")
        tracker.release()

        x = len(tracker.times())

        self.assertEqual(x, 10)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.time_interp(start = "1990/01/01", end = "1993/01/01", resolution = "x")

        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_error2(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.time_interp(end = "1993/01/01", resolution = "daily")
        n = len(nc.session_files())
        self.assertEqual(n, 0)


if __name__ == '__main__':
    unittest.main()

