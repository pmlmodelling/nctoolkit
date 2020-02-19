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

        n = len(nc.session_files())
        self.assertEqual(n, 1)

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

if __name__ == '__main__':
    unittest.main()

