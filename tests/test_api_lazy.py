import nctoolkit as nc
import pandas as pd
import glob
import xarray as xr
import os, pytest
import numpy as np
import platform

nc.options(lazy=True)


ff1 = "data/2003.nc"
ff2 = "data/2004.nc"


class TestApi2:
    def test_errors(self):
        ff1 = "data/2003.nc"
        ff2 = "data/2004.nc"

        ds = nc.open_geotiff("data/geotiff.tif")
        ds.spatial_mean()
        assert  ds.to_dataframe().Band1.values[0] == 215.0

        ds = nc.open_data([ff1, ff2], checks=False)
        ds.subset(time = 0)
        ds.run()

        assert ds.calendar == 'gregorian'

        assert "file 1" in list(ds.contents.reset_index().file)

        ff = "this_file_does_not_exist.nc"
        ff2 = "this_file_does_not_exist2.nc"

        with pytest.raises(FileNotFoundError):
            tracker = nc.open_data(ff, checks = False)

        with pytest.raises(FileNotFoundError):
            tracker = nc.open_data([ff, ff2])

        with pytest.raises(ValueError):
            nc.options(temp_dir = "/adsfjasdfiwnnck")

        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff, checks = False)
        assert tracker.contents.long_name[0] == 'Monthly Means of Global Sea Surface Temperature'
        tracker.assign(sst2 = lambda x: x.sst + 283)
        tracker.run()
        # linux only
        if platform.system() == "Linux":
            assert str(tracker.contents.long_name[1]) == "nan" 
        else:
            assert tracker.contents.long_name[1] == None 


        # check wildcard

        data = nc.open_data("data/*.nc", checks=False)  

        print([x for x in data if "" in x])
        assert [x for x in data if "data" in x] == [x for x in glob.glob("data/*.nc") if " " not in x]
        ff1 = "data/2003.nc"
        ff2 = "data/2004.nc"

        data1 = nc.open_data(ff1, checks=False)
        data2 = nc.open_data(ff2, checks=False)
        data = nc.cor_space(data1, data2)

        data.tmean()
        x = data.to_dataframe().cor.values[0].astype("float")

        data1.rename({"analysed_sst":"var1"})
        data1.subset(month =1)
        data2.rename({"analysed_sst":"var2"})
        data2.subset(month =1)
        data1.append(data2)
        data1.merge(match = "month")

        data1.cor_space("var1", "var2")
        y = data.to_dataframe().cor.values[0].astype("float")

        assert x == y

        with pytest.raises(TypeError):
            nc.options(parallel = "x")

        with pytest.raises(ValueError):
            nc.options(cores = 10000)

        with pytest.raises(ValueError):
            nc.options(precision = "x")

        with pytest.raises(TypeError):
            nc.options(cores = "x")

        with pytest.raises(TypeError):
            nc.options(lazy = "x")

        with pytest.raises(TypeError):
            nc.options(thread_safe = "x")

        ds = nc.open_data(ff1, checks=False)
        assert ds.current[0] == ds.start[0]

        ds1 = nc.open_data("data/ukesm_tas space.nc", checks=False)
        ds2 = nc.open_data("data/ukesm_tas.nc", checks=False)
        ds1-ds2
        ds1.spatial_sum()
        assert ds1.to_dataframe().tas.abs().sum() == 0.0






