import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_session(self):

        nc.options(lazy = True)
        x = nc.show_session()["lazy"]

        self.assertEqual(x, True)

        nc.options(cores = 3)
        x = nc.session.session_info["cores"]

        self.assertEqual(x, 3)


if __name__ == '__main__':
    unittest.main()

