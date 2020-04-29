import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


class TestAnomaly(unittest.TestCase):

    def test_relative(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.annual_anomaly(baseline = [1950, 1959])

        tracker.annual_anomaly(baseline = [1950, 1959], metric = "relative", window= 10)
        tracker.spatial_mean()
        tracker.select_years(1954)

        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 1.0)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_anomaly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.annual_anomaly(baseline = [1950, 1959])
        tracker.select_timestep(100)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -0.049895286560058594)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_monthly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.monthly_anomaly(baseline = [1950, 1959])
        tracker.select_timestep(100)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, -0.28783664107322693)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_error1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.annual_anomaly(baseline = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error2(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.monthly_anomaly(baseline = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error3(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.annual_anomaly(baseline = [1,2,3])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error4(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.monthly_anomaly(baseline = [1,2,3])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error5(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.annual_anomaly(baseline = [1,"x"])
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_error6(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.annual_anomaly(baseline = ["x","x"])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error7(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.annual_anomaly(baseline = [1990,1980])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error8(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.annual_anomaly(baseline = [1000,1990])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error9(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.annual_anomaly(baseline = [1980,1990], metric = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_error10(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.monthly_anomaly(baseline = [1,"x"])
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_error11(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.monthly_anomaly(baseline = ["x","x"])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error12(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.monthly_anomaly(baseline = [1990,1980])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error13(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.monthly_anomaly(baseline = [1000,1990])
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error_window(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.annual_anomaly(baseline = [1950, 1959], window = "x")
        with self.assertRaises(TypeError) as context:
            tracker.annual_anomaly(baseline = [1950, 1959], window = 0)



if __name__ == '__main__':
    unittest.main()

