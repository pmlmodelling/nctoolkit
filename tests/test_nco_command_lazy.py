import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(vars = "sst")
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncea -y mean", ensemble = True)
        print(data.current)
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

    def test_mean2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.mean()
        data.merge_time()
        data.mean()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncra -y mean", ensemble = False)

        data.merge_time()
        data.mean()
        data.spatial_mean()

        y = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

if __name__ == '__main__':
    unittest.main()

