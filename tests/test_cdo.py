import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_cdo(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cdo_command("DJF")
    def test_cdo1(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.cdo_command(1)

    def test_cdo2(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.cdo_command("-selmon,1 xy")


    def test_cdo3(self):
        tracker = nc.open_data(ff)
        tracker.cdo_command("chname,sst,tos")
        tracker.release()
        x = tracker.variables
        self.assertEqual(x, ["tos"])

    def test_cdo4(self):
        tracker = nc.open_data(ff)
        tracker.cdo_command("cdo -chname,sst,tos")
        tracker.release()
        x = tracker.variables
        self.assertEqual(x, ["tos"])


if __name__ == '__main__':
    unittest.main()

