import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestClean:
    def test_cleanall(self):
        safe = nc.session.nc_safe
        tracker = nc.open_data(ff)
        tracker.select_timesteps(0)
        tracker.run()
        safe = nc.session.nc_safe
        nc.clean_all()
        x = len([ff for ff in safe if os.path.exists(ff)])

        assert x == 0

    def test_empty(self):
        n = len(nc.session_files())

        assert n == 0
