import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os

nc.options(lazy = True)

ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_warning(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)

        with self.assertWarns(Warning):
            tracker.merge()

    def test_warning1(self):
        tracker = nc.open_data(ff)

        with self.assertWarns(Warning):
            tracker.merge_time()

    def test_warning2(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.release()
        new = nc.open_data(ff)
        new.select_timestep([0])
        new.rename({"sst":"tos"})
        new.release()
        data = nc.open_data([tracker.current, new.current])
        with self.assertWarns(Warning):
            data.merge(match = "year")



    def test_merge_time(self):
        nc.options(thread_safe = True)
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

    def test_merge(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.release()
        new = tracker.copy()
        new.rename({"sst":"tos"})
        new.release()
        data = nc.open_data([new.current, tracker.current])
        data.merge()
        data.mutate({"test1":"tos-sst"})
        data.spatial_mean()
        x = data.to_dataframe().test1.values[0]
        self.assertEqual(x, 0)

    def test_merge_error(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.release()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep(112)
        new.release()
        new.rename({"sst":"tos"})
        new.release()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge()

    def test_merge_error1(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.select_timestep([0])
        tracker.release()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep([0,1,2])
        new.release()
        new.rename({"sst":"tos"})
        new.release()
        data = nc.open_data([tracker.current, new.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = "month")

    def test_merge_error2(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1,2])
        tracker.release()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep(112)
        new.release()
        new.rename({"sst":"tos"})
        new.clip(lon = [50, 80])
        new.release()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = "year")

    def test_merge_error3(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.select_timestep([0, 1])
        tracker.release()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select_timestep([3,4])
        new.release()
        new.rename({"sst":"tos"})
        new.clip(lon = [50, 80])
        new.release()
        data = nc.open_data([new.current, tracker.current])
        with self.assertRaises(ValueError) as context:
            data.merge(match = ["year", "month"])

    def test_merge_error4(self):
        nc.options(thread_safe = True)
        tracker = nc.open_data(ff)
        tracker.release()
        new = tracker.copy()
        new.rename({"sst":"tos"})
        new.select_timestep([1,2,3,4])
        tracker.select_timestep([0,2,3,4])
        tracker.release()
        new.release()

        data = nc.open_data([new.current, tracker.current])

        with self.assertRaises(ValueError) as context:
            data.merge()



if __name__ == '__main__':
    unittest.main()

