import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os

nc.options(lazy = False)

ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_release(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.split(("year"))
        tracker.merge_time()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_dataframe().sst.values[0]
        nc.options(thread_safe = False)
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.release()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

