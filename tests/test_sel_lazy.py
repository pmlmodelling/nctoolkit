import unittest
import nchack as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_strvar(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+1"})
        tracker.select_variables("tos")
        tracker.run()
        x = tracker.variables
        self.assertEqual(x, ["tos"])

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.run()
        x = tracker.months()
        self.assertEqual(x, [1,2,12])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.run()
        x = tracker.months()
        self.assertEqual(x, [1])
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_months2(self):
        tracker = nc.open_data(ff)
        tracker.select_months(range(1,3))
        tracker.run()
        x = tracker.months()
        self.assertEqual(x, [1,2])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1990])

        n = len(nc.session_files())
        self.assertEqual(n, 1)
    def test_years_list(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1990])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1949, 1970])
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1970])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990,1993))
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1990,1991, 1992])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_years3(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1970, 1971])
        tracker.split("year")
        tracker.select_years([1970])
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1970])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timestep(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1970])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_timestep2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0, 13))
        tracker.run()
        x = tracker.years()
        self.assertEqual(x, [1970, 1971])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_montherror(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.select_months(0)

        with self.assertRaises(TypeError) as context:
            tracker.select_season(0)

        with self.assertRaises(ValueError) as context:
            tracker.select_months()

        with self.assertRaises(ValueError) as context:
            tracker.select_months(-1)

        with self.assertRaises(TypeError) as context:
            tracker.select_months(1.0)

        with self.assertRaises(TypeError) as context:
            tracker.select_years(1.0)

        with self.assertRaises(ValueError) as context:
            tracker.select_years()

        with self.assertRaises(TypeError) as context:
            tracker.select_years(0.1)

        with self.assertRaises(TypeError) as context:
            tracker.select_variables(0.1)

        with self.assertRaises(TypeError) as context:
            tracker.select_variables([0.1])

        with self.assertRaises(ValueError) as context:
            tracker.select_variables()

        with self.assertRaises(ValueError) as context:
            tracker.select_timestep()

        with self.assertRaises(TypeError) as context:
            tracker.select_timestep(0.1)

        with self.assertRaises(ValueError) as context:
            tracker.select_timestep(-1)



        with self.assertRaises(ValueError) as context:
            tracker.select_season()

        with self.assertRaises(ValueError) as context:
            tracker.select_season("x")


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
        tracker.run()
        x = tracker.variables
        self.assertEqual(x, ["sst", "tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_ensemble(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years()
        print(x)

        self.assertEqual(x, [1990])



if __name__ == '__main__':
    unittest.main()

