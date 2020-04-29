import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = False)


ff = "data/sst.mon.mean.nc"

class TestTimestat(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.percentile(p = "x")

        with self.assertRaises(ValueError) as context:
            tracker.percentile()

        with self.assertRaises(ValueError) as context:
            tracker.percentile(p = 120)


    def test_percentile(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.percentile(60)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.select_years([1990, 1991])
        tracker.split("year")
        tracker.percentile(60)
        tracker.select_years(1990)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)




    def test_sum(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)

        tracker1 = nc.open_data(ff)
        tracker1.select_timestep(1)

        tracker2 = nc.open_data(ff)
        tracker2.select_timestep([0,1])
        tracker2.sum()
        tracker2.spatial_sum()
        x = tracker2.to_dataframe().sst.values[0]
        tracker1.add(tracker)
        tracker1.spatial_sum()
        y = tracker1.to_dataframe().sst.values[0]

        self.assertEqual(x,y)


    def test_var(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0,12))

        tracker.var()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 3.090454578399658)

    def test_cum_sum(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0,12))

        tracker.cum_sum()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 12.710070610046387)



if __name__ == '__main__':
    unittest.main()

