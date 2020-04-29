import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestCor(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_cor(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.cor_space(var1 = "tos", var2 = "sst")
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cor_list(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.cor_space(var1 = "tos", var2 = "sst")
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cor1(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.cor_time(var1 = "tos", var2 = "sst")
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cor2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 2000))
        tracker.mutate({"tos":"sst+273.15"})
        tracker.split("year")
        tracker.cor_time(var1 = "tos", var2 = "sst")
        self.assertEqual(10, len(tracker.current))
        tracker.merge_time()
        self.assertEqual(10, len(tracker.years()))
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)




    def test_cor_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cor_space()
        n = len(nc.session_files())
        self.assertEqual(n, 0)

        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.mutate({"tos":"sst+273.15"})
        with self.assertRaises(ValueError) as context:
            tracker.cor_space(var1 = "x",  var2 = "y")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.mutate({"tos":"sst+273.15"})
        with self.assertRaises(ValueError) as context:
            tracker.cor_space(var1 = "tos", var2 = "y")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.cor_space(var1 = 1, var2 = "y")

        with self.assertRaises(TypeError) as context:
            tracker.cor_space(var1 = "x", var2 = 1)



if __name__ == '__main__':
    unittest.main()

