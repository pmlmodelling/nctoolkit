import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestClip:
    def test_clip(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.tmean()
        tracker.assign(sst = lambda x:  x.sst+273.15)
        tracker.compare(">0")
        tracker.spatial_sum()
        tracker.run()

        x = int(tracker.to_dataframe().sst.values[0].astype("float"))

        tracker = nc.open_data(ff, checks = False)
        tracker.tmean()
        tracker.run()
        new = tracker.copy()
        new.reduce_grid(tracker)

        y = len(
            new.to_dataframe().reset_index().loc[:, ["lon", "lat"]].drop_duplicates()
        )

        assert x == y

        new = tracker.copy()
        new.reduce_grid(tracker.current[0])

        y = len(
            new.to_dataframe().reset_index().loc[:, ["lon", "lat"]].drop_duplicates()
        )

        assert x == y

        with pytest.raises(ValueError):
            new.reduce_grid()

        with pytest.raises(ValueError):
            new.reduce_grid("xysadsfkji22.nc")
