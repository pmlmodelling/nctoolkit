import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import platform



from io import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
# This is a test to make sure we can change the temp dir to /var/tmp

class TestSession:

    def test_userdirs(self):

        with Capturing() as output:
            nc.utils.cdo_version()
        version = nc.session_info["cdo"]
        assert output[1] == f"nctoolkit is using Climate Data Operators version {version}" 

        # test version below

        assert nc.utils.version_below("2.0.4", "2.0.5")
        assert nc.utils.version_below("2.0.5", "2.0.5") is False


        # check whether netCDF variable names are valid
        assert nc.utils.name_check("") is False
        assert nc.utils.name_check(" ") is False
        assert nc.utils.name_check("1") is False
        assert nc.utils.name_check("a+") is False
        assert nc.utils.name_check("sst") is True
        assert nc.utils.name_check("sst1") is True
        assert nc.utils.name_check("sst_1") is True
        assert nc.utils.name_check("sst_1_2") is True


        # check whether netCDF variable names are valid






