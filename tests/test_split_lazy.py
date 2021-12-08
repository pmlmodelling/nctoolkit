import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


import subprocess


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"


class TestSplit:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_year(self):
        tracker = nc.open_data(ff)
        x = len(tracker.years)
        tracker.split("year")
        y = len(tracker.current)
        assert x == y
        n = len(nc.session_files())
        assert n == 30

    def test_yearmon(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times)
        tracker.split("yearmonth")
        y = len(tracker.current)
        assert x == y
        n = len(nc.session_files())
        assert n == y

    def test_yearmon(self):
        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        x = len(tracker.times)
        tracker.split("month")
        n = len(nc.session_files())
        assert n == 12

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.split("season")
        y = len(tracker.current)
        assert y == 4
        n = len(nc.session_files())
        assert n == y

    def test_day(self):
        ff1 = "data/2003.nc"
        tracker = nc.open_data(ff1)
        tracker.split("day")
        y = len(tracker.current)
        assert y == 31
        n = len(nc.session_files())
        assert n == y


    def test_error2(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.split("")

        n = len(nc.session_files())
        assert n == 0

    def test_list(self):
        tracker = nc.open_data(ff)
        x = len(tracker.times)
        tracker.split("year")
        tracker.split("yearmonth")
        y = len(tracker.current)
        assert x == y
        n = len(nc.session_files())
        assert n == y
