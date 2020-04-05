import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestSelect(unittest.TestCase):

    def test_year(self):
        tracker = nc.open_data(ff)
        x = len(tracker.years())
        tracker.split("year")
        y = len(tracker.current)
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 169)

    def test_yearmon(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times())
        tracker.split("yearmonth")
        y = len(tracker.current)
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, y)

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.split("season")
        y = len(tracker.current)
        self.assertEqual(y, 4)
        n = len(nc.session_files())
        self.assertEqual(n, y)


    def test_day(self):
        ff1 = "data/2003.nc"
        tracker = nc.open_data(ff1)
        tracker.split("day")
        y = len(tracker.current)
        self.assertEqual(y, 31)
        n = len(nc.session_files())
        self.assertEqual(n, y)

    def test_error(self):
        from pathlib import Path
        import os
        out = nc.temp_file.temp_file() + ".nc"
        Path(out).touch()

        with self.assertRaises(ValueError) as context:
            tracker = nc.open_data(out, checks = True)

        os.remove(out)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error2(self):
        print(nc.session_files())
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.split("")

        n = len(nc.session_files())
        self.assertEqual(n, 0)




    def test_list(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times())
        tracker.split("year")
        tracker.split("yearmonth")
        y = len(tracker.current)
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, y)


if __name__ == '__main__':
    unittest.main()

