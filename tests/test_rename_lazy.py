import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestRename(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_rename(self):
        tracker = nc.open_data(ff)
        tracker.rename({"sst":"tos"})
        tracker.run()
        x = tracker.variables
        self.assertEqual(x, ["tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_rename_error(self):
        tracker = nc.open_data(ff)
        tracker.run()
        with self.assertRaises(TypeError) as context:
            tracker.rename("sst")
        with self.assertRaises(TypeError) as context:
            tracker.rename({"sst":1})
        with self.assertRaises(TypeError) as context:
            tracker.rename({1:1})



        n = len(nc.session_files())
        self.assertEqual(n, 0)






if __name__ == '__main__':
    unittest.main()

