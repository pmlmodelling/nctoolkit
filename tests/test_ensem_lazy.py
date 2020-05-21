import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


class TestEnsemble(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_mean(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_mean(nco = True)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.996946334838867)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_max(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_max()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 19.205900192260742)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_min(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_min()
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 16.958738327026367)
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
        data.ensemble_mean( ignore_time = True)
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

        self.assertEqual(x, 2.2471628189086914 )
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_percent(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.ensemble_percentile(40)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, 17.851171493530273)
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
        data.release()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_warn2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_range()
        data.run()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_warn3(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        with self.assertWarns(Warning):
            data.ensemble_range()
        data.run()
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_pnone(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        with self.assertRaises(ValueError) as context:
            data.ensemble_percentile()

if __name__ == '__main__':
    unittest.main()

