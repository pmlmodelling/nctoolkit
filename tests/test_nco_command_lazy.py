import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


class TestNCO(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(vars = "sst")
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.nco_command("ncea -y mean", ensemble = True)
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

    def test_command_error(self):

        data = nc.open_data(nc.create_ensemble("data/ensemble"))

        with self.assertRaises(TypeError) as context:
            data.nco_command(1)

        with self.assertRaises(ValueError) as context:
            data.nco_command("test")
        with self.assertRaises(ValueError) as context:
            data.nco_command()



if __name__ == '__main__':
    unittest.main()

