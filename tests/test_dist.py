import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"



class TestDist:



    def test_dist(self):

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(time = 0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(time = 0)
        tracker.distribute(4,4)
        tracker.collect()
        #tracker.run()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")


        assert x == y
        n = len(nc.session_files())
        assert n == 1
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.distribute("x", "y")

        with pytest.raises(ValueError):
            tracker.distribute(-1, 1)

        with pytest.raises(ValueError):
            tracker.distribute(1, -1)

