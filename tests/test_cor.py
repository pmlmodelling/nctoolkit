import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_cor(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.cor_space()
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)

    def test_cor1(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sst+273.15"})
        tracker.cor_time()
        tracker.spatial_mean()
        x = tracker.to_dataframe().cor.values[0]

        self.assertEqual(x, 1.0)

if __name__ == '__main__':
    unittest.main()

