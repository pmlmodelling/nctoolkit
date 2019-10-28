import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_select(self):

        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.clip(lon = [-30, 20])
        tracker.clip(lat = [40, 70])
        tracker.time_interp(start = "1990-01-01", end = "1990-12-31", resolution = "daily")
        tracker.phenology("sst")
        tracker.spatial_mean()
        x = tracker.to_xarray().peak.values[0][0][0].astype("float")
        self.assertEqual(x, 214.74716186523438)

    def test_regrid1(self):
        ff = "/users/modellers/rwi/nchack/data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split_year_month()
        tracker.merge_time()
        tracker.split_year()
        tracker.merge_time()
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        grid = tracker.copy()
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        
        tracker = nc.open_data(ff)
        tracker.regrid(grid = grid, method = "nn")
        #tracker.annual_mean()
        tracker.split_year_month()
        tracker.ensemble_mean()
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, y) 



if __name__ == '__main__':
    unittest.main()

