import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestSelect:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_hours(self):
        ds = nc.open_data("data/hourly/01/swr_1997_01_01.nc", checks = False)
        ds.subset(hours = 3)
        ds.run()
        assert ds.times[0].hour == 3

    def test_levels(self):
        ds = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds.subset(levels = [0, 40])
        ds.run()
        assert ds.levels == [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]

        ds = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds.subset(levels = 5)
        
        ds.run()
        assert ds.levels == [5.0]


        ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
        ds.subset(time = 0)
        ds.run()
        for hour in range(3):
            ds1 = ds.copy()
            ds1.shift(hours = hour)
            ds.append(ds1)
        ds.merge("time")
        
        ds_test = ds.copy()
        
        ds_test = ds.copy()
        ds_test.subset(hour = 2)
        ds_test.run()
        assert [x.hour for x in ds_test.times][0] == 2
        
        ds_test = ds.copy()
        ds_test.subset(hour = range(1, 3))
        ds_test.run()
        assert [x.hour for x in ds_test.times] == [1,2]

        with pytest.raises(TypeError):
            ds_test.subset(hour = "a")

        with pytest.raises(ValueError):
            ds_test.subset(hour = 1000) 

        ds = nc.open_data("data/2003.nc", checks=False)
        ds.subset(day = 10)
        ds.run()
        assert len(ds.times) == 12
        
        ds = nc.open_data("data/2004.nc", checks=False)
        ds.subset(day = 31)
        ds.run()
        assert len(ds.times)  == 7
        
        ds = nc.open_data("data/2004.nc",  checks=False)
        ds.subset(day = range(1,3))
        ds.run()
        assert len(ds.times)  == 24

        with pytest.raises(ValueError):
            ds_test.subset(day = 1000) 
        with pytest.raises(ValueError):
            ds_test.subset(day = None) 

        with pytest.raises(TypeError):
            ds_test.subset(day = "a") 



    def test_range(self):
        ds = nc.open_data("data/200*.nc", checks = False)
        ds.merge("time")
        ds.subset(range = ["01/01/2003", "11/09/2004"])
        ds.run()
        assert len(ds.times) == 619

        ds = nc.open_data("data/200*.nc", checks=False)
        ds.merge("time")
        ds.subset(range = ["01-01-2003", "11-09-2004"])
        ds.run()
        assert len(ds.times) == 619

        ds = nc.open_data(ff, checks = False)
        with pytest.raises(TypeError):
            ds.subset(range = 1)

        ds = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            ds.subset(range = ["01/01/2003", "01/01/2002"])

        with pytest.raises(ValueError):
            ds.subset(range = ["01/01/2003/01", "01/01/2002"])
        with pytest.raises(ValueError):
            ds.subset(levels = "asdf")
        with pytest.raises(ValueError):
            ds.subset(levels = [1,"asdf"])
        with pytest.raises(ValueError):
            ds.subset(levels = [10,2])
        with pytest.raises(ValueError):
            ds.subset(range = None)

        with pytest.raises(ValueError):
            ds.subset(hours = None)

        with pytest.raises(ValueError):
            ds.subset(range = ["01/01/2003", 1])

        with pytest.raises(ValueError):
            ds.subset(range = ["01/01/2003", 1, 3])

    def test_strvar(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.subset(variables="tos")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]

    def test_season(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(seasons="DJF")
        tracker.run()
        x = tracker.months
        assert x == [1, 2, 12]
        n = len(nc.session_files())

        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(season = "DJF")
        tracker.run()
        x = tracker.months
        assert x == [1, 2, 12]
        n = len(nc.session_files())

        assert n == 1

    def test_months(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(months=1)
        tracker.run()
        x = tracker.months
        assert x == [1]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(month = 1)
        tracker.run()
        x = tracker.months
        assert x == [1]
        n = len(nc.session_files())
        assert n == 1

    def test_months2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(months=range(1, 3))
        tracker.run()
        x = tracker.months
        assert x == [1, 2]
        n = len(nc.session_files())
        assert n == 1

    def test_years(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]

        n = len(nc.session_files())
        assert n == 1

    def test_years_list(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.split("year")
        tracker.subset(years=1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.split("year")
        tracker.subset(year = 1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]
        n = len(nc.session_files())
        assert n == 1




    def test_years1(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=[1949, 1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_years2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=range(1990, 1993))
        tracker.run()
        x = tracker.years
        assert x == [1990, 1991, 1992]
        n = len(nc.session_files())
        assert n == 1

    def test_years3(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(years=[1970, 1971])
        tracker.split("year")
        tracker.subset(years=[1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(time = 0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(year = 1990, month = 1)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff, checks = False)
        tracker.subset(year = 1990)
        tracker.subset(month = 1)
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 1


    def test_timestepx23(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep2(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=range(0, 13))
        tracker.run()
        x = tracker.years
        assert x == [1970, 1971]
        n = len(nc.session_files())
        assert n == 1


    def test_timestep02(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.subset(timesteps=range(0, 13))
        tracker.run()
        x = tracker.years
        assert x == [1970, 1971]
        n = len(nc.session_files())
        assert n == 1


    def test_montherror(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.subset(months=0)

        with pytest.raises(ValueError):
            tracker.subset(season=None)

        with pytest.raises(ValueError):
            tracker.subset(years=None)

        with pytest.raises(ValueError):
            tracker.subset(months=None)

        with pytest.raises(ValueError):
            tracker.subset(variables=None)

        with pytest.raises(ValueError):
            tracker.subset(times=None)

        with pytest.raises(AttributeError):
            tracker.subset(problem = 0)

        with pytest.raises(TypeError):
            tracker.subset(seasons=0)

        with pytest.raises(ValueError):
            tracker.subset(months=-1)

        with pytest.raises(TypeError):
            tracker.subset(months=1.0)

        with pytest.raises(TypeError):
            tracker.subset(years=1.0)

        with pytest.raises(TypeError):
            tracker.subset(years=0.1)

        with pytest.raises(TypeError):
            tracker.subset(variables=0.1)

        with pytest.raises(TypeError):
            tracker.subset(variables=[0.1])

        with pytest.raises(TypeError):
            tracker.subset(timesteps=0.1)

        #with pytest.raises(ValueError):
        #    tracker.subset(timesteps=-1)

        with pytest.raises(ValueError):
            tracker.subset(seasons="x")

        n = len(nc.session_files())
        assert n == 0

    def test_missing_year(self):
        tracker = nc.open_data(ff, checks = False)
        with pytest.raises(ValueError):
            tracker.subset(years=1800)
            n = len(nc.session_files())
            assert n == 0

    def test_var_list(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.assign(tos1 =  lambda x: x.sst+1)
        tracker.subset(variables=["tos", "sst"])
        tracker.run()
        x = tracker.variables
        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff, checks = False)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.assign(tos1 =  lambda x: x.sst+1)
        tracker.subset(var = ["tos", "sst"])
        tracker.run()
        x = tracker.variables
        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1



    def test_ensemble(self):
        tracker = nc.open_data(ff, checks = False)
        tracker.split("year")
        tracker.merge("time")
        tracker.subset(years=1990)
        tracker.run()
        x = tracker.years

        assert x == [1990]
