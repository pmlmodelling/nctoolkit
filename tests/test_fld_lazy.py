import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestFldsta(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.spatial_percentile()


    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x,  18.02419662475586)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_max()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 30.430002212524414)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_min()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, -1.8530000448226929)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_range()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 32.28300094604492)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sum(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_sum()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x,  586924.6875)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_sum1(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_sum(by_area = True)

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x,6612921954074624.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_percent(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_percentile(p = 60)

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 19.700000762939453)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_percent_error(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.spatial_percentile(p = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            data.spatial_sum(by_area = 1)

    def test_percent_error2(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.spatial_percentile(p = 120)
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_ens(self):

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(range(0,6))
        data.split("yearmonth")
        data.spatial_sum(by_area = True)
        data.merge_time()
        data.mean()
        data.run()
        x = data.to_dataframe().sst.values[0]

        data = nc.open_data(ff)
        data.select_timestep(range(0,6))
        data.spatial_sum(by_area = True)
        data.mean()
        data.run()
        y = data.to_dataframe().sst.values[0]



        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

