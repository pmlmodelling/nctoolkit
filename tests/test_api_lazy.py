import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_cores(self):
        nc.options(cores = 6)
        x = nc.session.session_info["cores"]
        self.assertEqual(x, 6)

    def test_cores_error(self):
        with self.assertRaises(TypeError) as context:
            nc.options(cores = 6.1)

    def test_no_data(self):

        with self.assertRaises(ValueError) as context:
            data = nc.open_data("")

    def test_no_data2(self):

        with self.assertRaises(ValueError) as context:
            data = nc.open_data()

    def test_no_files1(self):

        with self.assertRaises(TypeError) as context:
            data = nc.open_data([1,2])


    def test_options_error(self):
        with self.assertRaises(ValueError) as context:
            nc.options(cores = 1000)

    def test_empty_list(self):
        with self.assertRaises(ValueError) as context:
            x = nc.open_data([])

    def test_missing_file_list(self):
        with self.assertRaises(ValueError) as context:
            x = nc.open_data(["none.nc"])


    def test_simplifying(self):
        ff = "data/sst.mon.mean.nc"
        with self.assertWarns(Warning):
            data = nc.open_data([ff, ff])

    def test_options_invalid(self):
        with self.assertRaises(AttributeError) as context:
            nc.options(this = 1)

    def test_options_invalid2(self):
        with self.assertRaises(AttributeError) as context:
            nc.options(lazy = "x")

    def test_file_size(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.api.file_size(ff)
        self.assertEqual(x, 525893626)

    def test_open_data(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)
        self.assertEqual(x.current, "data/sst.mon.mean.nc")

    def test_merge(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)

        y = nc.open_data(ff)
        y.rename({"sst":"tos"})
        z = nc.merge(x,y)
        z.release()
        test = z.variables

        self.assertEqual(test, ["sst", "tos"])




if __name__ == '__main__':
    unittest.main()

