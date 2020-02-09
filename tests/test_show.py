import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_levels(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        x = tracker.levels()

        self.assertEqual(len(x), 57)

    def test_nc_varaibles(self):
        ff = "data/woa18_decav_t01_01.nc"

        x = nc.nc_variables(ff)

        self.assertEqual(x, ['t_an', 't_dd', 't_gp', 't_ma', 't_mn', 't_oa', 't_sd', 't_se'])

    def test_times(self):
        ff = "data/sst.mon.mean.nc"

        tracker = nc.open_data(ff)
        x = tracker.times()

        self.assertEqual(len(x), 2028)

    def test_months(self):
        ff = "data/sst.mon.mean.nc"

        tracker = nc.open_data(ff)
        x = tracker.months()

        self.assertEqual(len(x), 12)

    def test_years(self):
        ff = "data/sst.mon.mean.nc"

        tracker = nc.open_data(ff)
        x = tracker.years()

        self.assertEqual(len(x), 169)


if __name__ == '__main__':
    unittest.main()

