import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestCreate:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_create(self):
        ensemble = nc.create_ensemble("data/ensemble")
        assert len(ensemble) == 60

        with pytest.raises(ValueError):
            ensemble = nc.create_ensemble("akdi2nkciihj2jkjjj")

        with pytest.raises(ValueError):
            ensemble = nc.create_ensemble(".", recursive=False)
