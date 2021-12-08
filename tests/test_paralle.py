import nctoolkit as nc
import platform
import subprocess
import pandas as pd
import xarray as xr
import os, pytest
import multiprocessing

nc.options(lazy=True)


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"


class TestPar:
    def test_parallel(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        n = len(nc.session_files())
        assert n == 0

        if platform.system() == "Linux":
            nc.options(cores = 2)
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.tmean()
        tracker.merge("time")
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst[0].astype("float")


        tracker = nc.open_data(ff)
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst[0].astype("float")

        assert x == y

        for ff in nc.session.get_safe():
            nc.session.remove_safe(ff)

        data = nc.open_data("data/ensemble/*.nc")
        data.spatial_sum(by_area = True)
        data.run()



        nc.options(cores = 1)






