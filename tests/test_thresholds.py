import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/2003.nc"


class TestClip:
    def test_thresholds(self):

        tracker = nc.open_data(ff)

        tracker = nc.open_data(ff)
        tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        tracker.last_below(350)
        tracker.set_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 349


        tracker = nc.open_data(ff)
        tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        tracker.first_above(350)
        tracker.set_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0




        tracker = nc.open_data(ff)
        tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        tracker.last_above(-351)
        tracker.set_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0



        tracker = nc.open_data(ff)
        tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        tracker.first_below(-351)
        tracker.set_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 351.0

