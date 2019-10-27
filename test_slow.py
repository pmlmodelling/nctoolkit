import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_select(self):

        ff = "/home/robert/Dropbox/nchack/data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.clip(lon = [-30, 20])
        tracker.clip(lat = [40, 70])
        tracker.time_interp(start = "1990-01-01", end = "1990-12-31", resolution = "daily")
        tracker.phenology("sst")
        tracker.spatial_mean()
        x = tracker.to_xarray().peak.values[0][0][0].astype("float")
        self.assertEqual(x, 214.74716186523438)



if __name__ == '__main__':
    unittest.main()

