import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestEnsemble(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(vars = "sst")
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.846817016601562)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_max(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 19.37936782836914)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_min()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 16.691144943237305)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_ignore_time(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(ignore_time = True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_ignore_time_2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(vars = "sst", ignore_time = True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.mean()
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_range(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_range()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 2.6882216930389404)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_percent(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_percentile(40)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.702301025390625)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_percent_error(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with self.assertRaises(TypeError) as context:
            data.ensemble_percentile("a")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_percent_error1(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with self.assertRaises(ValueError) as context:
            data.ensemble_percentile(129)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_mean_error(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with self.assertRaises(TypeError) as context:
            data.ensemble_mean(vars = 1)
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_warn(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_percentile(40)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_warn1(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_mean()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_warn2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_range()
        data.release()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_warn3(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_range()
        data.release()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_pnone(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with self.assertRaises(ValueError) as context:
            data.ensemble_percentile()

if __name__ == '__main__':
    unittest.main()

