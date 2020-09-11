import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestExpr:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_transmute(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.transmute({"tos": "sst+@inc"})
        tracker.run()
        x = tracker.variables

        assert x == ["tos"]

        n = len(nc.session_files())
        assert n == 1

    def test_sumall(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"tos": "sst+@inc"})
        tracker.sum_all()
        tracker.spatial_mean()
        x = tracker.to_xarray().total.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        assert x == y * 2

    def test_sumall_1(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"tos": "sst+@inc"})
        tracker.sum_all(drop=False)
        tracker.spatial_mean()
        x = tracker.to_xarray().total.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        assert x == y * 2

    def test_sumall_2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 0
        tracker.mutate({"total": "sst+@inc"})
        tracker.sum_all(drop=False)
        tracker.spatial_mean()
        x = tracker.to_xarray().total0.values[0][0][0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.spatial_mean()
        y = tracker.to_xarray().sst.values[0][0][0].astype("float")

        assert x == y * 2

    def test_mutate(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        inc = 273.15
        tracker.mutate({"tos": "sst+@inc"})
        tracker.run()
        x = tracker.variables

        assert x == ["sst", "tos"]
        n = len(nc.session_files())
        assert n == 1

    def test_localproblem(self):
        tracker = nc.open_data(ff)
        inc = "x"
        with pytest.raises(TypeError):
            tracker.transmute({"tos": "sst+@inc"})

        with pytest.raises(TypeError):
            tracker.mutate({"tos": "sst+@inc"})

        with pytest.raises(ValueError):
            tracker.mutate({"tos": "sst+@x"})

        with pytest.raises(ValueError):
            tracker.transmute({"tos": "sst+@x"})
        n = len(nc.session_files())
        assert n == 0

    def test_no_dict(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mutate("test")

        with pytest.raises(TypeError):
            tracker.transmute("test")
        n = len(nc.session_files())
        assert n == 0

    def test_badexpr1(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.mutate({"test": "sst&&1"})

    def test_doublesumall(self):
        tracker = nc.open_data(ff)
        tracker.sum_all()
        tracker.sum_all(drop=False)
        tracker.run()
        assert "total0" in tracker.variables
        tracker.sum_all(drop=False)
        tracker.run()
        assert "total1" in tracker.variables

    def test_error233(self):
        tracker = nc.open_data(ff)
        tracker.split("year")
        with pytest.raises(TypeError):
            tracker.sum_all()

        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.mutate({"x": 1})
        with pytest.raises(TypeError):
            tracker.mutate({2: 1})
