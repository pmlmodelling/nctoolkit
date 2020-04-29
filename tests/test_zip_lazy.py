import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os
import numpy as np


class TestZip(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_zip1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.release()
        new = tracker.copy()
        x = os.path.getsize(tracker.current)
        tracker.zip()
        tracker.release()
        y = os.path.getsize(tracker.current)
        z =  0.8 * x > y

        self.assertEqual(z, True)

        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        new.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x, y)


    def test_zip2(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.zip()
        tracker.release()
        new = tracker.copy()
        x = os.path.getsize(tracker.current)
        tracker.zip()
        tracker.release()
        y = os.path.getsize(tracker.current)
        z =  np.round(x/  y, 1).astype("float")

        self.assertEqual(z, 1)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        new.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x, y)



if __name__ == '__main__':
    unittest.main()

