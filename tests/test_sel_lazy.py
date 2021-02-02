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

    def test_strvar(self):
        tracker = nc.open_data(ff)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.select(variables="tos")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.select(seasons="DJF")
        tracker.run()
        x = tracker.months
        assert x == [1, 2, 12]
        n = len(nc.session_files())

        assert n == 1

        tracker = nc.open_data(ff)
        tracker.select(season = "DJF")
        tracker.run()
        x = tracker.months
        assert x == [1, 2, 12]
        n = len(nc.session_files())

        assert n == 1

    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select(months=1)
        tracker.run()
        x = tracker.months
        assert x == [1]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.select(month = 1)
        tracker.run()
        x = tracker.months
        assert x == [1]
        n = len(nc.session_files())
        assert n == 1

    def test_months2(self):
        tracker = nc.open_data(ff)
        tracker.select(months=range(1, 3))
        tracker.run()
        x = tracker.months
        assert x == [1, 2]
        n = len(nc.session_files())
        assert n == 1

    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]

        n = len(nc.session_files())
        assert n == 1

    def test_years_list(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.select(years=1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.select(year = 1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]
        n = len(nc.session_files())
        assert n == 1




    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select(years=[1949, 1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_years2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=range(1990, 1993))
        tracker.run()
        x = tracker.years
        assert x == [1990, 1991, 1992]
        n = len(nc.session_files())
        assert n == 1

    def test_years3(self):
        tracker = nc.open_data(ff)
        tracker.select(years=[1970, 1971])
        tracker.split("year")
        tracker.select(years=[1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.select(time = 0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1



    def test_timestepx23(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep2(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=range(0, 13))
        tracker.run()
        x = tracker.years
        assert x == [1970, 1971]
        n = len(nc.session_files())
        assert n == 1


    def test_timestep02(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=range(0, 13))
        tracker.run()
        x = tracker.years
        assert x == [1970, 1971]
        n = len(nc.session_files())
        assert n == 1


    def test_montherror(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.select(months=0)

        with pytest.raises(AttributeError):
            tracker.select(problem = 0)

        with pytest.raises(TypeError):
            tracker.select(seasons=0)

        with pytest.raises(ValueError):
            tracker.select(months=-1)

        with pytest.raises(TypeError):
            tracker.select(months=1.0)

        with pytest.raises(TypeError):
            tracker.select(years=1.0)

        with pytest.raises(TypeError):
            tracker.select(years=0.1)

        with pytest.raises(TypeError):
            tracker.select(variables=0.1)

        with pytest.raises(TypeError):
            tracker.select(variables=[0.1])

        with pytest.raises(TypeError):
            tracker.select(timesteps=0.1)

        with pytest.raises(ValueError):
            tracker.select(timesteps=-1)

        with pytest.raises(ValueError):
            tracker.select(seasons="x")

        n = len(nc.session_files())
        assert n == 0

    def test_missing_year(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.select(years=1800)
            n = len(nc.session_files())
            assert n == 0

    def test_var_list(self):
        tracker = nc.open_data(ff)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.assign(tos1 =  lambda x: x.sst+1)
        tracker.select(variables=["tos", "sst"])
        tracker.run()
        x = tracker.variables
        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.assign(tos =  lambda x: x.sst+1)
        tracker.assign(tos1 =  lambda x: x.sst+1)
        tracker.select(var = ["tos", "sst"])
        tracker.run()
        x = tracker.variables
        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1



    def test_ensemble(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.select(years=1990)
        tracker.run()
        x = tracker.years

        assert x == [1990]
