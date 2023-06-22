import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)

ff = "data/sst.mon.mean.nc"


class Testrun:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_run(self):
        print(nc.session.nc_safe)
        tracker = nc.open_data(ff, checks = False)
        tracker.split(("year"))
        tracker.merge("time")
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=0)
        tracker.spatial_mean()
        tracker.run()
        n = len(nc.session_files())
        y = tracker.to_dataframe().sst.values[0]

        assert x == y

        assert n == 1

        if nc.session.session_info["parallel"] == False:
            tracker = nc.open_data(ff, checks = False)
            tracker.tmean()
            tracker._safe.append("asdfkjasdkfj.nc")
            nc.session.nc_safe.append("asdfkjasdkfj.nc")
            tracker.run()
            print(nc.session.nc_safe)
            del tracker
            assert len(nc.session.nc_safe) == 0
