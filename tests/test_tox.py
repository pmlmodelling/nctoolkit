import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_setdate(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        x = tracker.to_xarray(decode_times = True).time.dt.year.values[0]

        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        y = tracker.to_xarray(decode_times = False).time.dt.year.values[0]

        self.assertEqual(x, y)



if __name__ == '__main__':
    unittest.main()

