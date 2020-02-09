import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_1(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.write_nc(ff1)
        data1 = nc.open_data(ff1)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)
        self.assertEqual(x,y)


    def test_2(self):
        ff = "data/sst.mon.mean.nc"
        ff1 = "/tmp/test.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.release()
        data.write_nc(ff1, zip = False)
        data1 = nc.open_data(ff1)

        data.spatial_mean()
        data1.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")
        y = data1.to_dataframe().sst.values[0].astype("float")
        os.remove(ff1)
        self.assertEqual(x,y)






if __name__ == '__main__':
    unittest.main()

