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

    def test_remove_variables(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.set_date(year=1990, month=1, day=1)
        tracker.mutate({"tos": "sst+273.15"})
        tracker.remove_variables("sst")
        tracker.run()
        x = tracker.variables

        assert x == ["tos"]

    def test_remove_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.remove_variables()
        with pytest.raises(TypeError):
            tracker.remove_variables([1])
