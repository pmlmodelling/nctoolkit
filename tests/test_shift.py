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


class TestShifters:
    def test_hours(self):
        data = nc.open_data(ff)
        data.shift_hours(-1)
        data.run()
        assert data.times[0] == "1969-12-31T23:00:00"

        data = nc.open_data(ff)
        data.shift(hours = -1)
        data.run()
        assert data.times[0] == "1969-12-31T23:00:00"

        data = nc.open_data(ff)
        data.shift(hours = -1.0)
        data.run()
        assert data.times[0] == "1969-12-31T23:00:00"

        data = nc.open_data(ff)
        data.shift_hours(-1.0)
        data.run()
        assert data.times[0] == "1969-12-31T23:00:00"

        data = nc.open_data(ff)
        with pytest.raises(TypeError):
            data.shift_hours()

        with pytest.raises(AttributeError):
            data.shift(none = "x")

        with pytest.raises(TypeError):
            data.shift_hours("x")
        with pytest.raises(TypeError):
            data.shift_days("x")
        with pytest.raises(TypeError):
            data.shift_months("x")
        with pytest.raises(TypeError):
            data.shift_years("x")


        with pytest.raises(TypeError):
            data.shift_hours()
        with pytest.raises(TypeError):
            data.shift_days()
        with pytest.raises(TypeError):
            data.shift_months()
        with pytest.raises(TypeError):
            data.shift_years()


        n = len(nc.session_files())
        assert n == 0

    def test_days(self):
        data = nc.open_data(ff)
        data.shift_days(1)
        data.run()
        assert data.times[0] == "1970-01-02T00:00:00"

        data = nc.open_data(ff)
        data.shift(days = 1)
        data.run()
        assert data.times[0] == "1970-01-02T00:00:00"

        data = nc.open_data(ff)
        data.shift(days = 1.0)
        data.run()
        assert data.times[0] == "1970-01-02T00:00:00"

        data = nc.open_data(ff)
        data.shift_days(1.0)
        data.run()
        assert data.times[0] == "1970-01-02T00:00:00"
        data = nc.open_data(ff)
        with pytest.raises(TypeError):
            data.shift_days()

        n = len(nc.session_files())
        assert n == 0

    def test_months(self):
        data = nc.open_data(ff)
        data.shift_months(1)
        data.run()
        assert data.times[0] == "1970-02-01T00:00:00"

        data = nc.open_data(ff)
        data.shift_months(1.0)
        data.run()
        assert data.times[0] == "1970-02-01T00:00:00"

        data = nc.open_data(ff)
        data.shift(months = 1)
        data.run()
        assert data.times[0] == "1970-02-01T00:00:00"


    def test_years(self):
        data = nc.open_data(ff)
        data.shift_years(1)
        data.run()
        assert data.times[0] == "1971-01-01T00:00:00"

        data = nc.open_data(ff)
        data.shift_years(1.0)
        data.run()
        assert data.times[0] == "1971-01-01T00:00:00"

        data = nc.open_data(ff)
        data.shift(years = 1)
        data.run()
        assert data.times[0] == "1971-01-01T00:00:00"



