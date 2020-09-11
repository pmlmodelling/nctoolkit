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
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.run()

        tracker.cell_areas()
        x = tracker.variables

        assert x == ["cell_area", "sst"]
        n = len(nc.session_files())

        assert n == 1

    def test_cell_areas2(self):
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1970, 1971)))
        tracker.select_months([1])
        tracker.cell_areas(join=False)
        tracker.run()

        x = tracker.variables

        assert x == ["cell_area"]
        n = len(nc.session_files())
        assert n == 1

    def test_cell_list(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0, 1])
        tracker.split("yearmonth")
        tracker.cell_areas(join=True)
        tracker.merge_time()
        tracker.run()
        x = tracker.variables
        assert x == ["cell_area", "sst"]
        n = len(nc.session_files())
        assert n == 1

    def test_error(self):
        tracker = nc.open_data(ff)
        tracker.cell_areas(join=True)
        with pytest.raises(ValueError):
            tracker.cell_areas(join=True)
        with pytest.raises(TypeError):
            tracker.cell_areas(join="x")
        n = len(nc.session_files())
        assert n == 1
