import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.mean.nc"

class TestClip(unittest.TestCase):

    def test_clip(self):
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.transmute({"sst":"sst+273.15"})
        tracker.compare_all(">0")
        tracker.spatial_sum()
        tracker.run()

        x = int(tracker.to_dataframe().sst.values[0].astype("float"))

        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.run()
        new = tracker.copy()
        new.reduce_grid(tracker)

        y = (len(new.to_dataframe().reset_index().loc[:,["lon", "lat"]].drop_duplicates()))

        assert x == y

        new = tracker.copy()
        new.reduce_grid(tracker.current)

        y = (len(new.to_dataframe().reset_index().loc[:,["lon", "lat"]].drop_duplicates()))

        assert x == y

        with self.assertRaises(ValueError) as context:
            new.reduce_grid()

        with self.assertRaises(ValueError) as context:
            new.reduce_grid("xysadsfkji22.nc")

if __name__ == '__main__':
    unittest.main()

