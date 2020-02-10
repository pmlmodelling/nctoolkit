import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_year(self):
        tracker = nc.open_data(ff)
        x = len(tracker.years())
        tracker.split("year")
        y = len(tracker.current)
        self.assertEqual(x, y)

    def test_yearmon(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times())
        tracker.split("yearmonth")
        y = len(tracker.current)
        self.assertEqual(x, y)

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.split("season")
        y = len(tracker.current)
        self.assertEqual(y, 4)


    def test_day(self):
        ff1 = "data/2003.nc"
        tracker = nc.open_data(ff1)
        tracker.split("day")
        y = len(tracker.current)
        self.assertEqual(y, 31)




if __name__ == '__main__':
    unittest.main()

