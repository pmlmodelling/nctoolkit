import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestShow(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_times(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0,12))
        tracker.run()
        x = len(tracker.times)

        self.assertEqual(x, 12)

    def test_times2(self):
        tracker = nc.open_data(ff)
        x = tracker.times
        tracker.split("year")
        y = tracker.times
        self.assertEqual(x,y)


    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select_months([1,2])
        tracker.run()
        x = tracker.months

        self.assertEqual(x, [1,2])

    def test_months1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990, 1991])
        tracker.select_months([1,2])
        tracker.split("year")
        tracker.run()
        x = tracker.months

        self.assertEqual(x, [1,2])


    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990,1999])
        tracker.run()
        x = tracker.years

        self.assertEqual(x, [1990,1999])

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990,1999])
        tracker.split("year")
        x = tracker.years

        self.assertEqual(x, [1990,1999])

    def test_nc_years(self):
        x = nc.nc_years(ff)

        self.assertEqual(len(x), len(range(1970, 2000)))

    def test_nc_variables(self):
        x = nc.nc_variables(ff)

        self.assertEqual(x, ["sst"])

    def test_levels(self):
        tracker = nc.open_data("data/woa18_decav_t01_01.nc")
        x = tracker.levels
        self.assertEqual([x[0], x[4]], [0.0,20.0])

    def test_levels2(self):
        tracker = nc.open_data(["data/woa18_decav_t01_01.nc","data/woa18_decav_t02_01.nc"])
        x = tracker.levels
        self.assertEqual([x[0], x[4]], [0.0,20.0])



if __name__ == '__main__':
    unittest.main()

