import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestShow:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_times(self):
        tracker = nc.open_data(ff)
        tracker.subset(timesteps=range(0, 12))
        tracker.run()
        x = len(tracker.times)
        assert x == 12

    def test_times2(self):
        tracker = nc.open_data(ff)
        x = tracker.times
        tracker.split("year")
        y = tracker.times
        assert x == y

    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.subset(months=[1, 2])
        tracker.run()
        x = tracker.months

        assert x == [1, 2]

    def test_months1(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=[1990, 1991])
        tracker.subset(months=[1, 2])
        tracker.split("year")
        tracker.run()
        x = tracker.months

        assert x == [1, 2]

    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=[1990, 1999])
        tracker.run()
        x = tracker.years

        assert x == [1990, 1999]

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=[1990, 1999])
        tracker.split("year")
        x = tracker.years

        assert x == [1990, 1999]

    def test_nc_years(self):
        x = nc.nc_years(ff)

        assert len(x) == len(range(1970, 2000))

    def test_nc_variables(self):
        x = nc.nc_variables(ff)

        assert x == ["sst"]

    def test_levels(self):
        tracker = nc.open_data("data/woa18_decav_t01_01.nc")
        x = tracker.levels
        assert [x[0], x[4]] == [0.0, 20.0]

    def test_levels2(self):
        tracker = nc.open_data(
            ["data/woa18_decav_t01_01.nc", "data/woa18_decav_t02_01.nc"]
        )
        x = tracker.levels
        assert [x[0], x[4]] == [0.0, 20.0]
