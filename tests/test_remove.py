import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestRemove:
    def test_remove_error(self):
        with pytest.raises(ValueError):
            nc.remove.nc_remove("/tmp/test.nc")

        with pytest.raises(ValueError):
            nc.remove.nc_remove("/tmp/nctoolkittest.nc")

        with pytest.raises(ValueError):
            nc.remove.nc_remove("/tmp/stamptest.nc")

        with pytest.raises(ValueError):
            nc.remove.nc_remove("stamptest.nc")

