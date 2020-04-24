import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_generate(self):
        x = nc.generate_ensemble("data/ensemble_merge")

        self.assertEqual(len(x), 2)

    def test_generate1(self):
        x = nc.generate_ensemble("data/ensemble")

        self.assertEqual(len(x), 1)


    def test_recurse(self):
        x = nc.generate_ensemble("data/ensemble1", recursive = True)
        y = nc.generate_ensemble("data/ensemble1/data", recursive = False)

        self.assertEqual(len(x), len(y))

        with self.assertRaises(ValueError) as context:
            z = nc.generate_ensemble("data/ensemble1/", recursive = False)

    def test_error1(self):
        with self.assertRaises(ValueError) as context:
            x = nc.generate_ensemble("test1928")


if __name__ == '__main__':
    unittest.main()

