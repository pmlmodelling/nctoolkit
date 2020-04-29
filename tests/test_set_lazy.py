import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_setdate(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 1, day = 1)
        tracker.release()
        x = tracker.years()[0]

        self.assertEqual(x, 1990)

        y = tracker.months()[0]

        self.assertEqual(y, 1)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_setdate2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 1, day = 1)
        tracker.release()
        x = tracker.years()[0]

        self.assertEqual(x, 1990)

        y = tracker.months()[0]

        self.assertEqual(y, 1)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_setdate3(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1951)))
        tracker.select_months([1])
        tracker.set_date(year = 1990, month = 3, day = 1)
        tracker.release()
        x = tracker.years()[0]

        self.assertEqual(x, 1990)

        y = tracker.months()[0]

        self.assertEqual(y, 3)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_setmissing(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_missing([0, 1000])
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x, -1.2176581621170044444)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


    def test_setmissing2(self):
        tracker = nc.open_data(ff)
        tracker.set_missing([100, 100])
        x = tracker.history

        tracker = nc.open_data(ff)
        tracker.set_missing(100)
        y = tracker.history




    def test_setunits(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_units({"sst":"C"})
        tracker.release()
        x = tracker.variables_detailed.units[0]

        self.assertEqual(x, "C")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_setmissing3(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.set_missing("x")

        with self.assertRaises(ValueError) as context:
            tracker.set_date()

        with self.assertRaises(ValueError) as context:
            tracker.set_date(year = 1990)

        with self.assertRaises(ValueError) as context:
            tracker.set_date(year = 1990, month = 1)


        with self.assertRaises(ValueError) as context:
            tracker.set_date(year = 1990, month = 1)

        with self.assertRaises(ValueError) as context:
            tracker.set_missing()

        with self.assertRaises(ValueError) as context:
            tracker.set_units()

        with self.assertRaises(TypeError) as context:
            tracker.set_units({"x":1})

        with self.assertRaises(TypeError) as context:
            tracker.set_units({1:1})


        with self.assertRaises(ValueError) as context:
            tracker.set_longnames()

        with self.assertRaises(TypeError) as context:
            tracker.set_longnames({"x":1})

        with self.assertRaises(TypeError) as context:
            tracker.set_longnames({1:1})

        with self.assertRaises(TypeError) as context:
            tracker.set_date(year = 1990, month = "x", day = 1)

        with self.assertRaises(TypeError) as context:
            tracker.set_date(year = "x", month = "x", day = 1)

        with self.assertRaises(TypeError) as context:
            tracker.set_date(year = 1, month = 1, day = "x")

        with self.assertRaises(TypeError) as context:
            tracker.set_missing([1,"x"])




        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_setunits2(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.set_units("x")
            n = len(nc.session_files())
            self.assertEqual(n, 0)

    def test_setattributes_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.set_attributes("x")
            n = len(nc.session_files())
            self.assertEqual(n, 0)

    def test_longname_error(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            tracker.set_longnames("x")
            n = len(nc.session_files())
            self.assertEqual(n, 0)


    def test_setlongnames(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months([1])

        tracker.set_longnames({"sst":"temp"})
        tracker.release()
        x = tracker.variables_detailed.long_name[0]

        self.assertEqual(x, "temp")
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_setlongnames2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.split("yearmonth")

        tracker.set_longnames({"sst":"temp"})
        tracker.merge_time()
        tracker.release()

        x = tracker.variables_detailed.long_name[0]

        self.assertEqual(x, "temp")
        n = len(nc.session_files())
        self.assertEqual(n, 1)



    def test_setattribute(self):
        tracker = nc.open_data(ff)
        tracker.set_attributes({"test123":"test"})
        x = "test123" in tracker.global_attributes()


        self.assertEqual(x, True)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_delete_attribute(self):
        tracker = nc.open_data(ff)
        y = tracker.global_attributes()
        tracker.set_attributes({"test123":"test"})
        x = "test123" in tracker.global_attributes()
        self.assertEqual(x, True)

        tracker.delete_attributes(["test123"])
        x = "test123" in tracker.global_attributes()

        self.assertEqual(x, False)
        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

