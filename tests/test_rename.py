import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_rename(self):
        tracker = nc.open_data(ff)
        tracker.rename({"sst":"tos"})
        tracker.release()
        x = tracker.variables
        self.assertEqual(x, ["tos"])

    def test_montherror(self):
        tracker = nc.open_data(ff)
        tracker.release()
        with self.assertRaises(TypeError) as context:
            tracker.rename("sst")






if __name__ == '__main__':
    unittest.main()

