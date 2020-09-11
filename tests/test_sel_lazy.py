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
        tracker.mutate({"tos": "sst+1"})
        tracker.select_variables("tos")
        tracker.run()
        x = tracker.variables
        assert x == ["tos"]

    def test_season(self):
        tracker = nc.open_data(ff)
        tracker.select_season("DJF")
        tracker.run()
        x = tracker.months
        assert x == [1, 2, 12]
        n = len(nc.session_files())

        assert n == 1

    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select_months(1)
        tracker.run()
        x = tracker.months
        assert x == [1]
        n = len(nc.session_files())
        assert n == 1

    def test_months2(self):
        tracker = nc.open_data(ff)
        tracker.select_months(range(1, 3))
        tracker.run()
        x = tracker.months
        assert x == [1, 2]
        n = len(nc.session_files())
        assert n == 1

    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]

        n = len(nc.session_files())
        assert n == 1

    def test_years_list(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years
        assert x == [1990]
        n = len(nc.session_files())
        assert n == 1

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1949, 1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_years2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(range(1990, 1993))
        tracker.run()
        x = tracker.years
        assert x == [1990, 1991, 1992]
        n = len(nc.session_files())
        assert n == 1

    def test_years3(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1970, 1971])
        tracker.split("year")
        tracker.select_years([1970])
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.run()
        x = tracker.years
        assert x == [1970]
        n = len(nc.session_files())
        assert n == 1

    def test_timestep2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0, 13))
        tracker.run()
        x = tracker.years
        assert x == [1970, 1971]
        n = len(nc.session_files())
        assert n == 1

    def test_montherror(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.select_months(0)

        with pytest.raises(TypeError):
            tracker.select_season(0)

        with pytest.raises(ValueError):
            tracker.select_months()

        with pytest.raises(ValueError):
            tracker.select_months(-1)

        with pytest.raises(TypeError):
            tracker.select_months(1.0)

        with pytest.raises(TypeError):
            tracker.select_years(1.0)

        with pytest.raises(ValueError):
            tracker.select_years()

        with pytest.raises(TypeError):
            tracker.select_years(0.1)

        with pytest.raises(TypeError):
            tracker.select_variables(0.1)

        with pytest.raises(TypeError):
            tracker.select_variables([0.1])

        with pytest.raises(ValueError):
            tracker.select_variables()

        with pytest.raises(ValueError):
            tracker.select_timestep()

        with pytest.raises(TypeError):
            tracker.select_timestep(0.1)

        with pytest.raises(ValueError):
            tracker.select_timestep(-1)

        with pytest.raises(ValueError):
            tracker.select_season()

        with pytest.raises(ValueError):
            tracker.select_season("x")

        n = len(nc.session_files())
        assert n == 0

    def test_missing_year(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.select_years(1800)
            n = len(nc.session_files())
            assert n == 0

    def test_var_list(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos": "sst+1"})
        tracker.mutate({"tos1": "sst+1"})
        tracker.select_variables(["tos", "sst"])
        tracker.run()
        x = tracker.variables
        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1

    def test_ensemble(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.select_years(1990)
        tracker.run()
        x = tracker.years

        assert x == [1990]
