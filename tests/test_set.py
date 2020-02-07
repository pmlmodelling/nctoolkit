import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_setdate(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 1, day = 1)
        tracker.release()
        x = tracker.years()[0]

        self.assertEqual(x, 1990)

        y = tracker.months()[0]

        self.assertEqual(y, 1)

    def test_setmissing(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_missing([0, 1000])
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x, -1.2176581621170044444)

    def test_setunits(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_units({"sst":"C"})
        tracker.release()
        x = tracker.variables_detailed.units[0]

        self.assertEqual(x, "C")


    def test_setlongnames(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_longnames({"sst":"temp"})
        tracker.release()
        x = tracker.variables_detailed.long_name[0]

        self.assertEqual(x, "temp")



if __name__ == '__main__':
    unittest.main()

