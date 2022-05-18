import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestCell:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_cell_areas(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()

        tracker.cell_area()
        x = tracker.variables

        assert x == ["cell_area", "sst"]
        print(tracker.history)
        n = len(nc.session_files())

        assert n == 1

    def test_cell_areas2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.cell_area(join=False)
        tracker.run()

        x = tracker.variables

        assert x == ["cell_area"]
        n = len(nc.session_files())
        assert n == 1

    def test_cell_list(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0, 1])
        tracker.split("yearmonth")
        tracker.cell_area(join=True)
        tracker.merge("time")
        tracker.run()
        x = tracker.variables
        assert x == ["cell_area", "sst"]
        n = len(nc.session_files())
        assert n == 1

    def test_error(self):
        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.cell_area(join=True)

        tracker = nc.open_data(ff)
        tracker.cell_area(join=True)
        with pytest.raises(ValueError):
            tracker.cell_area(join=True)
        with pytest.raises(TypeError):
            tracker.cell_area(join="x")
        n = len(nc.session_files())
        assert n == 1
