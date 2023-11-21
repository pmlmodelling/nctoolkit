import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestFldsta:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

        data = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            data.spatial_percentile()

    def test_mean(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0].astype("float")

        assert x == 12.573156356811523 
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_max()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == 23.31300163269043 
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_min()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == -1.6100001335144043 
        n = len(nc.session_files())
        assert n == 1


    def test_box(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(time = 0)
        data.box_mean(2,2)
        data.spatial_mean()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x ==  12.284067153930664 

        data = nc.open_data()
        with pytest.raises(ValueError):
            data.box_mean(2,2)

        with pytest.raises(ValueError):
            data.box_mean(-1,2)

        with pytest.raises(ValueError):
            data.box_mean(1,-1)

        with pytest.raises(ValueError):
            data.box_mean(1,"a")
        with pytest.raises(ValueError):
            data.box_mean("a",1)

        with pytest.raises(ValueError):
            data.spatial_mean()

        with pytest.raises(ValueError):
            data.spatial_sum()

        with pytest.raises(ValueError):
            data.spatial_percentile(p = 0.05)

        data = nc.open_data(ff, checks = False)
        data.subset(time = 0)
        data.box_sum(2,2)
        data.spatial_mean()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x ==  46.30331802368164 


        data = nc.open_data()
        with pytest.raises(ValueError):
            data.box_mean(2,2)

        data = nc.open_data(ff, checks = False)
        data.subset(time = 0)
        data.box_max(2,2)
        data.spatial_mean()

        x = data.to_dataframe().sst.values[0].astype("float")


        assert x == 12.64144229888916 

        data = nc.open_data(ff, checks = False)
        data.subset(time = 0)
        data.box_min(2,2)
        data.spatial_mean()

        x = data.to_dataframe().sst.values[0].astype("float")


        assert x == 11.918464660644531 


        data = nc.open_data(ff, checks = False)
        data.subset(time = 0)
        data.box_range(2,2)
        data.spatial_mean()

        x = data.to_dataframe().sst.values[0].astype("float")


        assert x == 0.7229775190353394 




    def test_range(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_range()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == 24.923002243041992 
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_sum()

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == 25770.927734375 
        n = len(nc.session_files())
        assert n == 1

    def test_sum1(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_sum(by_area=True)

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == 239103631163392.0 
        n = len(nc.session_files())
        assert n == 1

    def test_percent(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=0)
        data.spatial_percentile(p=60)

        x = data.to_dataframe().sst.values[0].astype("float")
        assert x == 14.437000274658203 
        n = len(nc.session_files())
        assert n == 1

    def test_percent_error(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            data.spatial_percentile(p="x")
        n = len(nc.session_files())
        assert n == 0
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            data.spatial_sum(by_area=1)

    def test_percent_error2(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            data.spatial_percentile(p=120)
        n = len(nc.session_files())
        assert n == 0

    def test_ens(self):

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=range(0, 6))
        data.split("yearmonth")
        data.spatial_sum(by_area=True)
        data.merge("time")
        data.tmean()
        data.run()
        x = data.to_dataframe().sst.values[0]

        data = nc.open_data(ff, checks = False)
        data.subset(timesteps=range(0, 6))
        data.spatial_sum(by_area=True)
        data.tmean()
        data.run()
        y = data.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

        ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
        ds.subset(time = 0)
        ds.spatial_stdev()
        assert float(ds.to_dataframe().sst.values[0]) == 5.8231096267700195 
        
        ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
        ds.subset(time = 0)
        ds.spatial_var()
        assert float(ds.to_dataframe().sst.values[0]) == 33.908607482910156 

