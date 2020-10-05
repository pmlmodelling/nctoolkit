import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)




class TestApi2:
    def test_errors(self):
        ff = "this_file_does_not_exist.nc"
        ff2 = "this_file_does_not_exist2.nc"

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)

        with pytest.raises(ValueError):
            tracker = nc.open_data([ff, ff2])
