import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestRemove(unittest.TestCase):

    def test_remove_error(self):
        with self.assertRaises(ValueError) as context:
            nc.remove.nc_remove("/tmp/test.nc")

        with self.assertRaises(ValueError) as context:
            nc.remove.nc_remove("/tmp/nctoolkittest.nc")

        with self.assertRaises(ValueError) as context:
            nc.remove.nc_remove("/tmp/stamptest.nc")

        with self.assertRaises(ValueError) as context:
            nc.remove.nc_remove("stamptest.nc")

        data = nc.open_data(ff)
        data.mean()
        data.run()
        with self.assertRaises(ValueError) as context:
            nc.remove.nc_remove(data.current)






if __name__ == '__main__':
    unittest.main()

