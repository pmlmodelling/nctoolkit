import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_clip(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lon = [-390, 100])


    def test_clip1(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lat = [-390, 100])

    def test_clip2(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lat = [-390, 100, 1])

    def test_clip3(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lat = [0, -10])

    def test_clip4(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lon = [0, -10])

    def test_clip5(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.mask_box(lon = [-390, 100, 1])

    def test_clip6(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lon = 1)

    def test_clip7(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lat = 1)

    def test_clip8(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lat = "1")

    def test_clip9(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lat = "2")

    def test_clip10(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lat = ["a",1 ])

    def test_clip11(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lat = [2, "b" ])

    def test_clip12(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lon = ["a",1 ])

    def test_clip13(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.mask_box(lon = [2, "b" ])



    def test_clip14(self):
        tracker = nc.open_data(ff)
        tracker.clip(lat = [0, 90], cdo = True)
        tracker.select_timestep(0)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")
        tracker = nc.open_data(ff)
        tracker.mask_box(lat = [0, 90])
        tracker.select_timestep(0)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x,y)


if __name__ == '__main__':
    unittest.main()

