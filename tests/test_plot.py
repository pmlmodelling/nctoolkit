import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest
import re

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"

class TestCrop:
    def test_plot(self):
        ds = nc.open_data(ff, checks = False)
        ds.subset(time = 0)
        out_file = nc.temp_file.temp_file(".html")
        ds.plot(out= out_file)
        file1 = open('data/test1.html', 'r')
        lines_1 = file1.readlines()
        file1 = open(out_file, 'r')
        lines_2 = file1.readlines()
        text = re.compile('"#.[0-9, a-z]*"')
        for i in range(len(lines_1)):
            assert text.findall(lines_1[i]) == text.findall(lines_2[i]) 
        os.remove(out_file)
