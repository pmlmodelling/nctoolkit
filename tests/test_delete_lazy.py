import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest

import warnings


ff = "data/sst.mon.mean.nc"


class TestDelete:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_drop(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.set_date(year=1990, month=1, day=1)
        tracker.assign(tos = lambda x: x.sst+273.15)
        tracker.drop(var = "sst")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]

        tracker = nc.open_data(ff)
        tracker.subset(time = [0,1, 2,3])
        tracker.drop(time = 0)
        tracker.run()
        assert len(tracker.times) == 3

        with pytest.raises(TypeError):
            tracker.drop(time = 1.2)

        with pytest.raises(TypeError):
            tracker.drop(variable = 1.2)

        ds = nc.open_data(ff, checks = False)
        ds.drop(year = 1970)
        ds.run()
        assert ds.years[0] == 1971
        ds.drop(month = 1)
        ds.run()
        assert ds.months[0] == 2

        ds.drop(month = range(1, 3))
        ds.run()
        assert ds.months[0] == 3

        ff1 = "data/2003.nc"
        ds = nc.open_data(ff1, checks = False)
        ds.drop(day = 1)
        ds.run()
        assert ds.times[0].day == 2

        with pytest.raises(TypeError):
            ds.drop(day = 1.2)




    def test_remove_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.drop()
        with pytest.raises(ValueError):
            tracker.drop(this = "that")
        with pytest.raises(TypeError):
            tracker.drop([1])
