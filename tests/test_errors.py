import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_clip(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.clip(lon = [-390, 100])


        with self.assertRaises(ValueError) as context:
            tracker.clip(lat = [-390, 100])


if __name__ == '__main__':
    unittest.main()

