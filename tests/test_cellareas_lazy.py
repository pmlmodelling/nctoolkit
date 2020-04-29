import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_cell_areas(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()

        tracker.cell_areas()
        x = tracker.variables


        self.assertEqual(x, ["sst", "cell_area"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cell_areas2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.cell_areas(join = False)
        tracker.release()

        x = tracker.variables


        self.assertEqual(x, [ "cell_area"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cell_list(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1])
        tracker.split("yearmonth")
        tracker.cell_areas(join = True)
        tracker.merge_time()
        tracker.release()
        x = tracker.variables
        self.assertEqual(x, [ "cell_area", "sst"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_error(self):
        tracker = nc.open_data(ff)
        tracker.cell_areas(join=True)
        with self.assertRaises(ValueError) as context:
            tracker.cell_areas(join=True)
        with self.assertRaises(TypeError) as context:
            tracker.cell_areas(join="x")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

