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

class TestShifters(unittest.TestCase):

    def test_hours(self):
        data = nc.open_data(ff)
        data.shift_hours(-1)
        data.run()
        assert data.times[0] == '1969-12-31T23:00:00'

        data = nc.open_data(ff)
        data.shift_hours(-1.0)
        data.run()
        assert data.times[0] == '1969-12-31T23:00:00'

        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            data.shift_hours()

        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_days(self):
        data = nc.open_data(ff)
        data.shift_days(1)
        data.run()
        assert data.times[0] == '1970-01-02T00:00:00'

        data = nc.open_data(ff)
        data.shift_days(1.0)
        data.run()
        assert data.times[0] == '1970-01-02T00:00:00'
        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            data.shift_days()

        n = len(nc.session_files())
        self.assertEqual(n, 0)



if __name__ == '__main__':
    unittest.main()

