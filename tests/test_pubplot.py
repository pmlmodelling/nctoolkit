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

        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.subset(time = 0)
        ds.pub_plot(out = out_file)

        with pytest.raises(ValueError, match=r"Did you mean"):
            ds.pub_plot(grid_colourrs = "none")

        with pytest.raises(ValueError, match=r"not a valid"):
            ds.pub_plot(invalid = None)

        assert os.path.exists(out_file)

        assert open("data/pubplot_test.png", "rb").read() == open(out_file, "rb").read()

        os.remove(out_file)
