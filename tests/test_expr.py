import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_transmute(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.transmute({"tos":"sst+@inc"})
        tracker.release()
        x = tracker.variables



        self.assertEqual(x, ["tos"])

    def test_mutate(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.mutate({"tos":"sst+@inc"})
        tracker.release()
        x = tracker.variables



        self.assertEqual(x, ["sst", "tos"])

if __name__ == '__main__':
    unittest.main()

