import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = False)


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_clim1(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "peak")
        data.spatial_mean()

        x = data.to_dataframe().peak.values[0].astype("float")

        self.assertEqual(x, 5.104045391082764)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_start_mid(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "middle")
        data.spatial_mean()

        x = data.to_dataframe().middle.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start", p = 50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        self.assertEqual(x, y)

    def test_start_end(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "end", p = 50)
        data.spatial_mean()

        x = data.to_dataframe().end.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start", p = 50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        self.assertEqual(x, y)


    def test_error(self):
        data = nc.open_data(ff)

        with self.assertRaises(ValueError) as context:
            data.phenology("sst", metric = "this")

        with self.assertRaises(ValueError) as context:
            data.phenology("sst", metric = "peak")
        with self.assertRaises(ValueError) as context:
            data.phenology("sst", metric = "middle")

        n = len(nc.session_files())
        self.assertEqual(n, 0)

        with self.assertRaises(TypeError) as context:
            data.phenology("sst", metric = "start", p = "2")




    def test_typeerror(self):
        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            data.phenology(var = 1, metric = "peak")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_nometricerror(self):
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.phenology("sst")

        with self.assertRaises(ValueError) as context:
            data.phenology(metric = "peak")


    def test_defaults(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "end")
        data.spatial_mean()

        x = data.to_dataframe().end.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start", p = 75)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        self.assertEqual(x, y)

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start")
        data.spatial_mean()

        x = data.to_dataframe().start.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start", p = 25)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        self.assertEqual(x, y)


        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "middle")
        data.spatial_mean()

        x = data.to_dataframe().middle.values[0].astype("float")

        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst", metric = "start", p = 50)
        data.spatial_mean()

        y = data.to_dataframe().start.values[0].astype("float")

        self.assertEqual(x, y)




if __name__ == '__main__':
    unittest.main()

