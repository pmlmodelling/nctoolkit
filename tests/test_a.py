import pandas as pd
import xarray as xr
import os, pytest

import importlib
import nctoolkit as nc
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

ff = "data/sst.mon.mean.nc"


class TestFinal:
    def test_a(self):

        assert len(nc.session_files()) == 0
        assert len(nc.session.get_safe()) == 0

        ds = nc.open_data(ff, checks = False)
        with Capturing() as output:
            ds.check()

        output == ['*****************************************',
         'Checking data types',
         '*****************************************',
         'Variable checks passed',
         '*****************************************',
         'Checking time data type',
         '*****************************************',
         '*****************************************',
         'Running CF-compliance checks',
         '*****************************************',
         '*****************************************',
         'Checking grid consistency',
         '*****************************************']


