import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):




    def test_add(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.add(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + 1, y)

        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_add2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 2)


    def test_add_var(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.mutate({"tos":"sst+1-1"})
        tracker.release()
        new.add(tracker, var = "tos")
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 2)



    def test_add3(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(tracker.current)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(x + x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_subtract(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(1)
        new.subtract(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(y, 1)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_subtract1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(1)
        new.subtract(tracker.current)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        self.assertEqual(y, 1)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_op_list(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        new = nc.open_data(ff)
        new.select_timestep([0,1])
        new.split("yearmonth")
        new.subtract(data)
        new.merge_time()
        new.select_timestep(0)
        new.spatial_sum()
        x = new.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x,0.0)
        n = len(nc.session_files())
        self.assertEqual(n, 2)


    def test_subtract2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.subtract(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x - 1, y)
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_multiply(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.multiply(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(np.round(x * 10, 4).astype("float"), np.round(y, 4).astype("float"))
        n = len(nc.session_files())
        self.assertEqual(n, 2)

    def test_multiply1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.multiply(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y*2)
        n = len(nc.session_files())
        self.assertEqual(n, 3)


    def test_multiply2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker.current)
        out = tracker.copy()
        tracker.multiply(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y*2)
        n = len(nc.session_files())
        self.assertEqual(n, 3)



    def test_divide(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        tracker.spatial_mean()
        new.divide(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(np.round(x / 10, 4), np.round(y, 4))
        n = len(nc.session_files())
        self.assertEqual(n, 2)


    def test_divide1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y/2)
        n = len(nc.session_files())
        self.assertEqual(n, 3)


    def test_divide2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.release()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker.current)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        self.assertEqual(x, y/2)
        n = len(nc.session_files())
        self.assertEqual(n, 3)



    def test_file_incompat(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(ValueError) as context:
            tracker.add(ff2)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat1(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(ValueError) as context:
            tracker.subtract(ff2)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat2(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(ValueError) as context:
            tracker.divide(ff2)
        n = len(nc.session_files())
        self.assertEqual(n, 0)



    def test_file_incompat3(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.multiply("xyz")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat4(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.subtract("xyz")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat5(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.add("xyz")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat6(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.divide("xyz")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_incompat7(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(ValueError) as context:
            tracker.multiply(ff2)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_typeerror(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(TypeError) as context:
            tracker.multiply([1,2])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_typeerror1(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(TypeError) as context:
            tracker.subtract([1,2])
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_typeerror2(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(TypeError) as context:
            tracker.add([1,2])

        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_file_typeerror3(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with self.assertRaises(TypeError) as context:
            tracker.divide([1,2])
        n = len(nc.session_files())
        self.assertEqual(n, 0)


if __name__ == '__main__':
    unittest.main()

