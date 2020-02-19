import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os
import warnings


class TestSelect(unittest.TestCase):

    def test_mean(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 6.885317325592041)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_max()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 10.37883186340332)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_min()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 4.02338171005249 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sum(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_sum()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 416.1104736328125)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_range()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 6.35545015335083)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_int(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_interp(vert_depths=10)
        x =tracker.to_dataframe().t_an.values[0].astype("float")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_surface(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        tracker.surface()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        self.assertEqual(x, 9.660191535949707)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_bottom(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        tracker.bottom()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        self.assertEqual(x, 4.494192123413086)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_bottom_error(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        new = tracker.copy()
        new.rename({"t_an":"test"})
        new.release()
        test = nc.open_data([tracker.current, new.current])
        with self.assertWarns(Warning):
            test.bottom()
        n = len(nc.session_files())
        self.assertEqual(n, 2)

if __name__ == '__main__':
    unittest.main()

