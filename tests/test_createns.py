import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_generate(self):
        x = nc.generate_ensemble("data/ensemble_merge")

        self.assertEqual(len(x), 2)

    def test_generate1(self):
        x = nc.generate_ensemble("data/ensemble")

        self.assertEqual(len(x), 1)



if __name__ == '__main__':
    unittest.main()

