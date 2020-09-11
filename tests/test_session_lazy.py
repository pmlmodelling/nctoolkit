import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestSession:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_session(self):

        nc.options(lazy=True)
        assert nc.show_session()["lazy"]

        nc.options(cores=2)
        x = nc.session.session_info["cores"]
        nc.options(cores=1)

        assert x == 2
