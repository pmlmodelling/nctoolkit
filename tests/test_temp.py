import nctoolkit as nc
import subprocess
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)




ff = "data/sst.mon.mean.nc"


class TestTemp:
    def test_temp(self):
        with pytest.raises(TypeError):
            nc.temp_file.temp_file(1)
