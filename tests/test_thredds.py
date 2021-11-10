import pandas as pd
import xarray as xr
import os, pytest

import importlib
import nctoolkit as nc

ff = "data/sst.mon.mean.nc"


class TestFinal:
    def test_a(self):

        if os.path.exists("tests/local.txt"):
            ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.ltm.1981-2010.nc")
            contents = ds.contents

            assert contents.long_name[1] ==  "count of non-missing values used in mean"


