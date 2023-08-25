import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestRename:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_rename(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.rename({"sst": "tos"})
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.rename(tos =  "sst")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]
        n = len(nc.session_files())
        assert n == 1

        # is warning raised
        with pytest.warns(UserWarning):
            tracker = nc.open_data(ff, checks = False)
            tracker.subset(times = [0,1])
            tracker.split("month")
            tracker.rename({"tos": "sstsdf"})





    def test_rename_error(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.run()
        with pytest.raises(TypeError):
            tracker.rename("sst")
        with pytest.raises(ValueError):
            tracker.rename({"sst":"+sst+++"})
        with pytest.raises(ValueError):
            tracker.rename({"+++sst+++":"sst"})

        with pytest.raises(TypeError):
            tracker.rename({"sst":1})
        with pytest.raises(TypeError):
            tracker.rename({1:"sst"})

        with pytest.raises(TypeError):
            tracker.rename({"sst": 1})
        with pytest.raises(TypeError):
            tracker.rename({1: 1})

        n = len(nc.session_files())
        assert n == 0
