import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestClean:
    def test_cleanall(self):
        safe = nc.session.get_safe()
        print([ff for ff in safe if os.path.exists(ff)])
        tracker = nc.open_data(ff)
        tracker.select(timesteps=0)
        tracker.run()
        safe = nc.session.get_safe()
        print([ff for ff in safe if os.path.exists(ff)])
        nc.clean_all()
        print([ff for ff in safe if os.path.exists(ff)])
        x = len([ff for ff in safe if os.path.exists(ff)])

        assert x == 0

    def test_empty(self):
        n = len(nc.session_files())

        assert n == 0
