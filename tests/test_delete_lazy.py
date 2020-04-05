import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os

import warnings


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_remove_variables(self):
        tracker = nc.open_data(ff)
        print("This: " + nc.nc_variables(ff)[0])
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 1, day = 1)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.remove_variables("sst")
        tracker.release()
        x = tracker.variables
        print(x)

        self.assertEqual(x, ["tos"])

    def test_remove_variables1(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.release()
        with self.assertWarns(Warning):
            tracker.remove_variables("tos")

    def test_remove_variables2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.mutate({"tos":"sst+1"})
        tracker.release()
        with self.assertWarns(Warning):
            tracker.remove_variables(["tos", "test"])

    def test_remove_variables3(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.mutate({"tos":"sst+1"})
        tracker.release()
        with self.assertWarns(Warning):
            tracker.remove_variables(["tos", "test", "test2"])

if __name__ == '__main__':
    unittest.main()

