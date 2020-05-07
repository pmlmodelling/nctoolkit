import unittest
import nchack as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestCdo(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)
    def test_cdo(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cdo_command("DJF")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_cdo_nocommand(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cdo_command()

    def test_cdo1(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.cdo_command(1)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_cdo2(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cdo_command("-selmon,1 xy")
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_cdo3(self):
        tracker = nc.open_data(ff)
        tracker.cdo_command("chname,sst,tos")
        tracker.run()
        x = tracker.variables
        self.assertEqual(x, ["tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cdo4(self):
        tracker = nc.open_data(ff)
        tracker.cdo_command("cdo -chname,sst,tos")
        tracker.run()
        x = tracker.variables
        self.assertEqual(x, ["tos"])
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_cdo5(self):
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.cdo_command("-mergetime")
        tracker.mean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]
        n = len(nc.session_files())
        self.assertEqual(n, 1)


        self.assertEqual(x, y)

if __name__ == '__main__':
    unittest.main()

