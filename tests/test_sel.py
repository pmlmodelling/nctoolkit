import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.release()
        x = tracker.months()
        self.assertEqual(x, [1,2,12])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.release()
        x = tracker.months()
        self.assertEqual(x, [1])
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_months2(self):
        tracker = nc.open_data(ff)
        tracker.select_months(range(1,3))
        tracker.release()
        x = tracker.months()
        self.assertEqual(x, [1,2])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1990])

        n = len(nc.session_files())
        self.assertEqual(n, 1)
    def test_years_list(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.select_years(1990)
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1990])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1849, 1850])
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1850])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990,1993))
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1990,1991, 1992])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years3(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1850, 1851])
        tracker.split("year")
        tracker.select_years([1850])
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1850])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timestep(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1850])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timestep2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0, 13))
        tracker.release()
        x = tracker.years()
        self.assertEqual(x, [1850, 1851])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_montherror(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.select_months(0)
            n = len(nc.session_files())
            self.assertEqual(n, 0)

    def test_missing_year(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.select_years(1800)
            n = len(nc.session_files())
            self.assertEqual(n, 0)

    def test_var_list(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+1"})
        tracker.mutate({"tos1":"sst+1"})
        tracker.select_variables(["tos", "sst"])
        tracker.release()
        x = tracker.variables
        self.assertEqual(x, ["sst", "tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)





if __name__ == '__main__':
    unittest.main()

