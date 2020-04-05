import unittest
import nchack as nc
nc.options(lazy= False)
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
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_montherror(self):
        tracker = nc.open_data(ff)
        tracker.release()
        with self.assertRaises(TypeError) as context:
            tracker.rename("sst")
            n = len(nc.session_files())
            self.assertEqual(n, 0)






if __name__ == '__main__':
    unittest.main()

