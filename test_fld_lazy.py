import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestFldsta(unittest.TestCase):



    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x,  18.02419662475586)
        #n = len(nc.session_files())
        #self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

