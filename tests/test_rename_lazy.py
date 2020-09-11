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
        tracker = nc.open_data(ff)
        tracker.rename({"sst": "tos"})
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]
        n = len(nc.session_files())
        assert n == 1

    def test_rename_error(self):
        tracker = nc.open_data(ff)
        tracker.run()
        with pytest.raises(TypeError):
            tracker.rename("sst")
        with pytest.raises(TypeError):
            tracker.rename({"sst": 1})
        with pytest.raises(TypeError):
            tracker.rename({1: 1})

        n = len(nc.session_files())
        assert n == 0
