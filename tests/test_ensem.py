import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.846817016601562)


    def test_max(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 19.37936782836914)

    def test_min(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_min()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 16.691144943237305)


    def test_range(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_range()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 2.6882216930389404)


    def test_percent(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_percentile(40)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.702301025390625)



if __name__ == '__main__':
    unittest.main()

