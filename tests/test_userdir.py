import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import platform


ff = "data/sst.mon.mean.nc"

# This is a test to make sure we can change the temp dir to /var/tmp

class TestSession:

    def test_userdirs(self):

        if platform.system() == "Linux":
            nc.options(temp_dir ="/var/tmp")
            nc.options(lazy=False)
            data = nc.open_data(ff)
            data.spatial_mean()
            data.mean()
            nc.options(lazy=True)

            data = nc.open_data(ff)
            data.spatial_mean()
            data.mean()
            data.run()
            assert data.current.startswith("/var/tmp")
            nc.options(temp_dir = "/tmp")
            del data
            nc.cleanup()
            n = len(nc.session_files())
            assert n == 0
