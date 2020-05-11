import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSession(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_session(self):

        nc.options(lazy = True)
        x = nc.show_session()["lazy"]

        self.assertEqual(x, True)

        nc.options(cores = 2)
        x = nc.session.session_info["cores"]
        nc.options(cores = 1)

        self.assertEqual(x, 2)


if __name__ == '__main__':
    unittest.main()

