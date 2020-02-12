import unittest
import nchack as nc
nc.options(lazy= True)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os
import warnings


class TestSelect(unittest.TestCase):

    def test_warning(self):
        ff = "data/sst.mon.mean.nc"

        out_file = nc.temp_file.temp_file(".nc")
        cdo_command = "cdo selyear,1800,1900 " + ff + " " + out_file
        with self.assertWarns(Warning):
            out_file = nc.runthis.run_cdo(cdo_command, target = out_file)

        os.remove(out_file)

    def test_warning2(self):
        ff = "data/sst.mon.mean.nc"

        out_file = nc.temp_file.temp_file(".nc")
        cdo_command = "cdo selmon,12,13 " + ff + " " + out_file
        with self.assertWarns(Warning):
            out_file = nc.runthis.run_cdo(cdo_command, target = out_file)

        os.remove(out_file)
if __name__ == '__main__':
    unittest.main()

