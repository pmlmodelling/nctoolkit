import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os

nc.options(lazy = True)

ff = "data/sst.mon.mean.nc"

class TestMerge(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_warning(self):
        tracker = nc.open_data(ff)

        with self.assertWarns(Warning):
            tracker.merge()
        tracker.run()
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_warning1(self):
        tracker = nc.open_data(ff)

        with self.assertWarns(Warning):
            tracker.merge_time()
        tracker.run()
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_warning2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.run()
        new = nc.open_data(ff)
        new.select_timestep([0])
        new.rename({"sst":"tos"})
        new.run()
        data = nc.open_data([tracker.current, new.current])
        with self.assertWarns(Warning):
            data.merge(match = "year")

        data.run()

        n = len(nc.session_files())
        self.assertEqual(n, 3)


    def test_merge_time(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_merge(self):
        tracker = nc.open_data(ff)
        tracker.run()
        new = tracker.copy()
        new.rename({"sst":"tos"})
        new.run()
        data = nc.open_data([new.current, tracker.current])
        data.merge()
        data.mutate({"test1":"tos-sst"})
        data.spatial_mean()
        x = data.to_dataframe().test1.values[0]
        self.assertEqual(x, 0)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_merge_error(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep(112)
        new.run()
        new.rename({"sst":"tos"})
        new.run()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge()



        n = len(nc.session_files())
        self.assertEqual(n, 2)

        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(TypeError) as context:
            data.merge(match = 1)

    def test_merge_error1(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep([0,1,2])
        new.run()
        new.rename({"sst":"tos"})
        new.run()
        data = nc.open_data([tracker.current, new.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = "month")

        with self.assertRaises(TypeError) as context:
            data.merge( match = [1])

        with self.assertRaises(ValueError) as context:
            data.merge( match = "test")

        with self.assertRaises(ValueError) as context:
            data.merge()

        with self.assertRaises(TypeError) as context:
            data = nc.open_data([tracker.current, new.current], match = 1)

        n = len(nc.session_files())

        tracker = nc.open_data(ff)

    def test_merge_error2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep(112)
        new.run()
        new.rename({"sst":"tos"})
        new.clip(lon = [50, 80])
        new.run()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = "year")
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_merge_error3(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0, 1])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep([3,4])
        new.run()
        new.rename({"sst":"tos"})
        new.clip(lon = [50, 80])
        new.run()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = ["year", "month"])
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_merge_error4(self):
        tracker = nc.open_data(ff)
        tracker.run()
        new = tracker.copy()
        new.rename({"sst":"tos"})
        new.select_timestep([1,2,3,4])
        tracker.select_timestep([0,2,3,4])
        tracker.run()
        new.run()

        data = nc.open_data([new.current, tracker.current])

        with self.assertRaises(ValueError) as context:
            data.merge()
        n = len(nc.session_files())
        self.assertEqual(n, 2)



if __name__ == '__main__':
    unittest.main()

