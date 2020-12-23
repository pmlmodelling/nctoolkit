import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestClip:
    def test_centre(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.centre("test")
        n = len(nc.session_files())
        assert n == 0

        with pytest.raises(TypeError):
            tracker.centre(by_area = 1)

        tracker = nc.open_data(ff)
        tracker.centre("longitude")
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == 192.1805877685547

        tracker = nc.open_data(ff)
        tracker.centre("latitude")
        x = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == -6.278953552246094

        n = len(nc.session_files())
        assert n == 1



