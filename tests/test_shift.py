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
        data = nc.open_data(ff, checks = False)
        data.shift(hours=-1)
        data.run()
        assert str(data.times[0]) == "1969-12-31 23:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(hours = -1)
        data.run()
        assert str(data.times[0]) == "1969-12-31 23:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(hours = -1.0)
        data.run()
        assert str(data.times[0]) == "1969-12-31 23:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(hours=-1.0)
        data.run()
        assert str(data.times[0]) == "1969-12-31 23:00:00"


        with pytest.raises(AttributeError):
            data.shift(none = "x")

        with pytest.raises(ValueError):
            data.shift(hours=None)
        with pytest.raises(ValueError):
            data.shift(days=None)
        with pytest.raises(ValueError):
            data.shift(months=None)
        with pytest.raises(ValueError):
            data.shift(years=None)

        with pytest.raises(TypeError):
            data.shift(hours="x")
        with pytest.raises(TypeError):
            data.shift(days="x")
        with pytest.raises(TypeError):
            data.shift(months="x")
        with pytest.raises(TypeError):
            data.shift(years="x")



    def test_days(self):
        data = nc.open_data(ff, checks = False)
        data.shift(days=1)
        data.run()
        assert str(data.times[0]) == "1970-01-02 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(days = 1)
        data.run()
        assert str(data.times[0]) == "1970-01-02 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(days = 1.0)
        data.run()
        assert str(data.times[0]) == "1970-01-02 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(days=1.0)
        data.run()
        assert str(data.times[0]) == "1970-01-02 00:00:00"
        data = nc.open_data(ff, checks = False)

        with pytest.raises(TypeError):
            data.shift(days="x")


    def test_months(self):
        data = nc.open_data(ff, checks = False)
        data.shift(months=1)
        data.run()
        assert str(data.times[0])  == "1970-02-01 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(months=1.0)
        data.run()
        assert str(data.times[0]) == "1970-02-01 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(months = 1)
        data.run()
        assert str(data.times[0]) == "1970-02-01 00:00:00"


    def test_years(self):
        data = nc.open_data(ff, checks = False)
        data.shift(years=1)
        data.run()
        assert str(data.times[0]) == "1971-01-01 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(years=1.0)
        data.run()
        assert str(data.times[0]) == "1971-01-01 00:00:00"

        data = nc.open_data(ff, checks = False)
        data.shift(years = 1)
        data.run()
        assert str(data.times[0]) == "1971-01-01 00:00:00"



