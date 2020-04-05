import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)



ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_reduce(self):
        nc.options(lazy = False)
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.reduce_dims()
        n = len(tracker.times())
        print(nc.session.session_info)
        self.assertEqual(n, 0)
        nc.options(lazy = True)




if __name__ == '__main__':
    unittest.main()

