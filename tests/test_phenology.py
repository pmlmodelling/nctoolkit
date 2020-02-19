import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_clim1(self):
        data = nc.open_data(ff)
        data.select_timestep(list(range(0, 12)))
        data.phenology("sst")
        data.spatial_mean()
        x = data.to_dataframe().peak.values[0].astype("float")



        self.assertEqual(x, 5.104045391082764)
        n = len(nc.session_files())
        self.assertEqual(n, 1)



    def test_error(self):
        data = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            data.phenology()
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_typeerror(self):
        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            data.phenology(var = 1)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

if __name__ == '__main__':
    unittest.main()

