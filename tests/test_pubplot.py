import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest
import re


ff = "data/sst.mon.mean.nc"

class TestCrop:
    def test_plot(self):

        # generate a random file name
        out_file = "asdfkjbuwnjlajksdfi.png"

        ds = nc.open_data("data/sst.mon.mean.nc", checks = False)
        ds.subset(time = 0)
        ds.pub_plot(out = out_file, land = "grey")

        with pytest.raises(ValueError, match=r"Did you mean"):
            ds.pub_plot(grid_colourrs = "none")

        with pytest.raises(ValueError, match=r"not a valid"):
            ds.pub_plot(invalid = None)

        assert os.path.exists(out_file)
        # get file size
        # this needs to be improved so it figures if the file is similar to the one in the repo
        assert os.path.getsize(out_file) > 160000 and os.path.getsize(out_file) < 170000


        # value error check

        with pytest.raises(ValueError):
            ds.pub_plot(legend_position = "blah")

        with pytest.raises(ValueError):
            ds.pub_plot(scale = "blah")

        with pytest.raises(ValueError):
            ds.pub_plot(coast = "blah")

        ds1 = ds.copy()
        ds1.assign(tos = lambda x: x.sst + 273.15)

        with pytest.raises(ValueError):
            ds1.pub_plot()
        with pytest.raises(ValueError):
            ds1 = nc.open_data("data/sst.mon.mean.nc", checks = False)
            ds1.pub_plot()


        from difflib import SequenceMatcher

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        os.remove(out_file)
