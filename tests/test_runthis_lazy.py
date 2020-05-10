import unittest
import nchack as nc
nc.options(lazy= False)
import pandas as pd
import xarray as xr
import os
import warnings
import subprocess

cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cdo_check = str(cdo_check.stderr).replace("\\n", "")
cdo_check = cdo_check.replace("b'", "").strip()
cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]


class TestRunthis(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_warning(self):

        if cdo_version not in ["1.9.7", "1.9.8"]:
            return None
        ff = "data/sst.mon.mean.nc"

        out_file = nc.temp_file.temp_file(".nc")
        cdo_command = "cdo selyear,1800,1970 " + ff + " " + out_file
        with self.assertWarns(Warning):
            out_file = nc.runthis.run_cdo(cdo_command, target = out_file)

        os.remove(out_file)

    def test_warning2(self):
        # cdo does not trigger a warning in version 1.9.6
        if cdo_version not in ["1.9.7", "1.9.8"]:
            return None
        ff = "data/sst.mon.mean.nc"

        out_file = nc.temp_file.temp_file(".nc")
        cdo_command = "cdo selmon,12,13 " + ff + " " + out_file
        with self.assertWarns(Warning):
            out_file = nc.runthis.run_cdo(cdo_command, target = out_file)

        os.remove(out_file)

    def test_nco_invalid(self):
        ff = "data/sst.mon.mean.nc"

        out_file = nc.temp_file.temp_file(".nc")
        with self.assertRaises(ValueError) as context:
            out_file = nc.runthis.run_nco("test", target = out_file)

if __name__ == '__main__':
    unittest.main()

