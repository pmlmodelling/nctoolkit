import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestCrop:
    def test_crop(self):
        tracker = nc.open_data(["data/ukesm_tas.nc", "data/ukesm_gpp.nc"])
        tracker.merge()
        tracker.cor_time("tas", "gpp")
        tracker.run()
        tracker.spatial_range()
        y = tracker.to_dataframe().cor.values[0].astype("float")
        assert y == 1.9630122184753418

