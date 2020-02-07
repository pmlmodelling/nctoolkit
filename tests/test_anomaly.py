import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_anomaly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.annual_anomaly(baseline = [1950, 1959])
        tracker.select_timestep(100)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -0.049895286560058594)

    def test_monthly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.monthly_anomaly(baseline = [1950, 1959])
        tracker.select_timestep(100)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -0.28783664107322693)
if __name__ == '__main__':
    unittest.main()

