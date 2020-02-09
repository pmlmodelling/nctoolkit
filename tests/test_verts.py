import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_mean(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 6.885317325592041)

    def test_max(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_max()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 10.37883186340332)

    def test_min(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_min()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 4.02338171005249 )

    def test_range(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_range()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        self.assertEqual(x, 6.35545015335083)

    def test_int(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_interp(vert_depths=10)
        x =tracker.to_dataframe().t_an.values[0].astype("float")

    def test_surface(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        tracker.surface()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        self.assertEqual(x, 9.660191535949707)

    def test_bottom(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        tracker.bottom()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        self.assertEqual(x, 4.494192123413086)

if __name__ == '__main__':
    unittest.main()

