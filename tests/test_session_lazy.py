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

        nc.session.append_protected("foo.nc")
        assert "foo.nc" in nc.session.nc_protected
        nc.session.remove_protected("foo.nc")
        assert "foo.nc" not in nc.session.nc_protected

        nc.options(lazy=True)
        assert nc.session.session_info["lazy"]

        nc.options(cores=2)
        x = nc.session.session_info["cores"]
        nc.options(cores=1)

        assert x == 2
