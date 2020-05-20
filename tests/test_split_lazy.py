import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


import subprocess
def cdo_version():
    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]

ff = "data/sst.mon.mean.nc"

class TestSplit(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_year(self):
        tracker = nc.open_data(ff)
        x = len(tracker.years)
        tracker.split("year")
        y = len(tracker.current)
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 30)

    def test_yearmon(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times)
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

        # do not run the check below for cdo 1.9.5 as the behaviour is not the same there
        if cdo_version() not in ["1.9.5"]:
            with self.assertRaises(ValueError) as context:
                tracker = nc.open_data(out, checks = True)

        tracker = nc.open_data(out)
        with self.assertRaises(ValueError) as context:
            tracker.split()


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
        x = len(tracker.times)
        tracker.split("year")
        tracker.split("yearmonth")
        y = len(tracker.current)
        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, y)


if __name__ == '__main__':
    unittest.main()

