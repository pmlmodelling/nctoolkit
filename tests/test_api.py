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


    def test_options_error(self):
        with self.assertRaises(ValueError) as context:
            nc.options(cores = 1000)



if __name__ == '__main__':
    unittest.main()

