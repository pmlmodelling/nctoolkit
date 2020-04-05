import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_clim1(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.ensemble_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff)
        tracker.monthly_mean_climatology()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -1.7077397108078003)
        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_clim2(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.clip(lon = [50, 60])
        tracker.ensemble_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff)
        tracker.monthly_mean_climatology()
        tracker.clip(lon = [50, 60])
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 19.814777374267578)
        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cdocommand(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        tracker = nc.open_data(ff)
        tracker.cdo_command("cdo selmon,1")
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        n = len(nc.session_files())
        self.assertEqual(n, 1)

        self.assertEqual(x, y)

    def test_percentile(self):
        tracker = nc.open_data(ff)
        tracker.clip(lon = [50, 60])
        tracker.percentile(50)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 19.51475715637207)

        n = len(nc.session_files())
        self.assertEqual(n, 1)



if __name__ == '__main__':
    unittest.main()

