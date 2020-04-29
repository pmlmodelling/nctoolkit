import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestExpr(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_transmute(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.transmute({"tos":"sst+@inc"})
        tracker.release()
        x = tracker.variables



        self.assertEqual(x, ["tos"])

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sumall(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"tos":"sst+@inc"})
        tracker.sum_all()
        tracker.spatial_mean()
        x = tracker.to_xarray().total.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        self.assertEqual(x, y * 2)


    def test_sumall_1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"tos":"sst+@inc"})
        tracker.sum_all(drop = False)
        tracker.spatial_mean()
        x = tracker.to_xarray().total.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        self.assertEqual(x, y * 2)

    def test_sumall_2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"total":"sst+@inc"})
        tracker.sum_all(drop = False)
        tracker.spatial_mean()
        x = tracker.to_xarray().total0.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        self.assertEqual(x, y * 2)

    def test_mutate(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.mutate({"tos":"sst+@inc"})
        tracker.release()
        x = tracker.variables



        self.assertEqual(x, ["sst", "tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_localproblem(self):
        tracker = nc.open_data(ff)
        inc = "x"
        with self.assertRaises(TypeError) as context:
            tracker.transmute({"tos":"sst+@inc"})

        with self.assertRaises(TypeError) as context:
            tracker.mutate({"tos":"sst+@inc"})

        with self.assertRaises(ValueError) as context:
            tracker.mutate({"tos":"sst+@x"})

        with self.assertRaises(ValueError) as context:
            tracker.transmute({"tos":"sst+@x"})
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_no_dict(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mutate("test")

        with self.assertRaises(TypeError) as context:
            tracker.transmute("test")
        n = len(nc.session_files())
        self.assertEqual(n, 0)




    def test_badexpr1(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mutate({"test":"sst&&1"})

    def test_doublesumall(self):
        tracker = nc.open_data(ff)
        tracker.sum_all()
        tracker.sum_all(drop = False)
        tracker.release()
        x = "total0" in tracker.variables
        self.assertEqual(x, True)
        tracker.sum_all(drop = False)
        tracker.release()
        x = "total1" in tracker.variables
        self.assertEqual(x, True)

    def test_error233(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        with self.assertRaises(TypeError) as context:
            tracker.sum_all()

        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mutate({"x":1})
        with self.assertRaises(TypeError) as context:
            tracker.mutate({2:1})


if __name__ == '__main__':
    unittest.main()

