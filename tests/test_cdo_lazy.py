import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import subprocess


ff = "data/sst.mon.mean.nc"


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


class TestCdo:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_cdo(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.cdo_command("DJF")
        n = len(nc.session_files())
        assert n == 0

    def test_cdo_nocommand(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.cdo_command()

    def test_cdo1(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.cdo_command(1)
        n = len(nc.session_files())
        assert n == 0

    def test_cdo2(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.cdo_command("-selmon,1 xy")
        n = len(nc.session_files())
        assert n == 0

    def test_cdo3(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.cdo_command("chname,sst,tos")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]
        n = len(nc.session_files())
        assert n == 1

    def test_cdo4(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.cdo_command("cdo -chname,sst,tos")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]
        n = len(nc.session_files())
        assert n == 1

    def test_cdo5(self):
        if cdo_version() in ["1.9.2", "1.9.3"]:
            return None
        tracker = nc.open_data(ff, checks = False)
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff, checks = False)
        tracker.split("year")
        tracker.cdo_command("-mergetime")
        tracker.tmean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data("data/ensemble/*.nc", checks=False)
        tracker.ensemble_mean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data("data/ensemble/*.nc", checks=False)
        tracker.cdo_command("-ensmean", ensemble = True)
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]
        n = len(nc.session_files())



        assert x == y





