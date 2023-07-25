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


        from difflib import SequenceMatcher

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()


#        x = str(open("data/pubplot_test.png", "rb").read())[0:2000]
#        y = str(open(out_file, "rb").read())[0:2000]
#
#        assert similar(x, y) > 0.96
#
 

        # assert open("data/pubplot_test.png", "rb").read() == open(out_file, "rb").read()

        os.remove(out_file)
