import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_remove_variables(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 1, day = 1)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.remove_variables("sst")
        tracker.release()
        x = tracker.variables

        self.assertEqual(x, ["tos"])


if __name__ == '__main__':
    unittest.main()

