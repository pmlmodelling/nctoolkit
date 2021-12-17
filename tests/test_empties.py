import nctoolkit as nc
import subprocess
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]




ff = "data/sst.mon.mean.nc"


class TestClip:
    def test_zonal1(self):
        ds = nc.open_data()

        with pytest.raises(ValueError):
            ds.tmean()

        with pytest.raises(ValueError):
            ds.tpercentile()

        with pytest.raises(ValueError):
            ds.cor_time("x1", "x2")
