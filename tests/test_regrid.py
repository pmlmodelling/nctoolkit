import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_regrid(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.regrid(new, method = "nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

    def test_montherror(self):
        tracker = nc.open_data(ff)
        tracker.release()
        with self.assertRaises(ValueError) as context:
            tracker.regrid()


    def test_regrid1(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        grid = new.to_dataframe().reset_index().loc[:,["lon", "lat"]]

        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.regrid(grid, method = "nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

    def test_regrid2(self):
        ff = "data/sst.mon.mean.nc"
        grid = nc.open_data(ff)
        grid.select_timestep(0)
        grid.clip(lon = [0, 90], lat = [0, 90])

        tracker = nc.open_data(ff)
        tracker.select_years(1850)
        tracker.mean()
        tracker.regrid(grid)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years(1850)
        tracker.split("yearmonth")
        tracker.regrid(grid)
        tracker.ensemble_mean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x, y)





if __name__ == '__main__':
    unittest.main()

