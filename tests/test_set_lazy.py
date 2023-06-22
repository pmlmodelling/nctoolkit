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


class TestSetters:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

        ds = nc.open_data("data/2003.nc")
        ds.subset(time = 0)
        ds.set_year(2010)
        ds.run()
        assert ds.years[0] == 2010

        with pytest.raises(ValueError):
            ds.set_year("a")
        with pytest.raises(ValueError):
            ds.set_day("a")

        with pytest.raises(ValueError):
            ds.set_precision("a")
        ds.set_precision("F64")
        ds.run()
        assert ds.contents.data_type[0] == "F64"
        assert ds._precision == "default"

        ds = nc.open_data(ff, checks = False)
        ds.subset(time = 0)
        ds.set_day(15)
        ds.run()
        assert [x.day for x in ds.times][0] == 15

    def test_setdate(self):

        # do not run this test with cdo version 1.9.3 as there is a bug
        if cdo_version() not in ["1.9.3"]:
            tracker = nc.open_data(ff, checks = False)
            tracker.subset(years=list(range(1970, 1971)))
            tracker.subset(months=[1])
            tracker.set_date(year=1990, month=1, day=1)
            tracker.run()
            x = tracker.years[0]

            assert x == 1990

            y = tracker.months[0]

            assert y == 1
            n = len(nc.session_files())
            assert n == 1

    def test_setdate2(self):
        if cdo_version() not in ["1.9.3"]:
            tracker = nc.open_data(ff, checks = False)
            tracker.subset(years=list(range(1970, 1971)))
            tracker.subset(months=[1])
            tracker.set_date(year=1990, month=1, day=1)
            tracker.run()
            x = tracker.years[0]

            assert x == 1990

            y = tracker.months[0]

            assert y == 1
            n = len(nc.session_files())
            assert n == 1

    def test_setdate3(self):
        if cdo_version() not in ["1.9.3"]:
            tracker = nc.open_data(ff, checks = False)
            tracker.subset(years=list(range(1970, 1971)))
            tracker.subset(months=[1])
            tracker.set_date(year=1990, month=3, day=1)
            tracker.run()
            x = tracker.years[0]

            assert x == 1990

            y = tracker.months[0]
            assert y == 3

            n = len(nc.session_files())
            assert n == 1

    def test_setmissing(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.subset(months=[1])

        tracker.as_missing([0, 1000])
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_dataframe().sst.values[0]

        assert x == -0.7675796747207642 
        n = len(nc.session_files())
        assert n == 1

    def test_setmissing2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.as_missing([100, 100])
        x = tracker.history

        tracker = nc.open_data(ff, checks = False)
        tracker.as_missing(100)
        y = tracker.history

    def test_setunits(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.subset(months=[1])

        tracker.set_units({"sst": "C"})
        tracker.run()
        x = tracker.contents.unit[0]

        assert x == "C"
        n = len(nc.session_files())
        assert n == 1

    def test_setmissing3(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.as_missing("x")

        with pytest.raises(ValueError):
            tracker.set_date()

        with pytest.raises(ValueError):
            tracker.set_date(year=1990)

        with pytest.raises(ValueError):
            tracker.set_date(year=1990, month=1)

        with pytest.raises(ValueError):
            tracker.set_date(year=1990, month=1)

        with pytest.raises(ValueError):
            tracker.as_missing()

        with pytest.raises(ValueError):
            tracker.set_units()

        with pytest.raises(TypeError):
            tracker.set_units({"x": 1})

        with pytest.raises(TypeError):
            tracker.set_units({1: 1})

        with pytest.raises(ValueError):
            tracker.set_longnames()

        with pytest.raises(TypeError):
            tracker.set_longnames({"x": 1})

        with pytest.raises(TypeError):
            tracker.set_longnames({1: 1})

        with pytest.raises(TypeError):
            tracker.set_date(year=1990, month="x", day=1)

        with pytest.raises(TypeError):
            tracker.set_date(year="x", month="x", day=1)

        with pytest.raises(TypeError):
            tracker.set_date(year=1, month=1, day="x")

        with pytest.raises(TypeError):
            tracker.as_missing([1, "x"])

        n = len(nc.session_files())
        assert n == 0

    def test_setunits2(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.set_units("x")
            n = len(nc.session_files())
            assert n == 0

    def test_longname_error(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            tracker.set_longnames("x")
            n = len(nc.session_files())
            assert n == 0

    def test_setlongnames(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.subset(months=[1])

        tracker.set_longnames({"sst": "temp"})
        tracker.run()
        x = tracker.contents.long_name[0]

        assert x == "temp"
        n = len(nc.session_files())
        assert n == 1

    def test_setlongnames2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.split("yearmonth")

        tracker.set_longnames({"sst": "temp"})
        tracker.merge("time")
        tracker.run()

        x = tracker.contents.long_name[0]

        assert x == "temp"
        n = len(nc.session_files())
        assert n == 1
