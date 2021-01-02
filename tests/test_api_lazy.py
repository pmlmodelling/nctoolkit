import nctoolkit as nc
import pandas as pd
import glob
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff1 = "data/2003.nc"
ff2 = "data/2004.nc"


class TestApi2:
    def test_errors(self):
        ff = "this_file_does_not_exist.nc"
        ff2 = "this_file_does_not_exist2.nc"

        with pytest.raises(ValueError):
            tracker = nc.open_data(ff)

        with pytest.raises(ValueError):
            tracker = nc.open_data([ff, ff2])

        with pytest.raises(ValueError):
            nc.options(temp_dir = "/adsfjasdfiwnnck")


        # check wildcard

        data = nc.open_data("data/*.nc")

        assert data.current == glob.glob("data/*.nc")
        ff1 = "data/2003.nc"
        ff2 = "data/2004.nc"

        data1 = nc.open_data(ff1)
        data2 = nc.open_data(ff2)
        data = nc.cor_space(data1, data2)

        data.tmean()
        x = data.to_dataframe().cor.values[0].astype("float")

        data1.rename({"analysed_sst":"var1"})
        data1.select(month =1)
        data2.rename({"analysed_sst":"var2"})
        data2.select(month =1)
        data1.append(data2)
        data1.merge(match = "month")


        data1.cor_space("var1", "var2")
        y = data.to_dataframe().cor.values[0].astype("float")

        assert x == y







