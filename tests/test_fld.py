import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.669960021972656)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_max()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 30.30000114440918)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_min()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, -1.8540000915527344)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_range()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 32.15399932861328)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_sum(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_sum()

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 575101.3125)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_sum1(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_sum(by_area = True)

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 6482955169955840.0 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_percent(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_percentile(p = 60)

        x = data.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 19.628000259399414)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_percent_error(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.spatial_percentile(p = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

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
        data.release()
        print(data.current)
        x = data.to_dataframe().sst.values[0]

        data = nc.open_data(ff)
        data.select_timestep(range(0,6))
        data.spatial_sum(by_area = True)
        data.mean()
        data.release()
        print(data.current)
        y = data.to_dataframe().sst.values[0]



        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

