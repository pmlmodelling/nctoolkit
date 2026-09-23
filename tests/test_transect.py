import nctoolkit as nc
import numpy as np
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestTransect:
    def test_transect(self):
        start = [-70, 40]
        end = [-20, 55]
        nsteps = 10

        ds = nc.open_data(ff, checks=False)
        ds.subset(time=0)
        ds.to_transect(start=start, end=end, nsteps=nsteps)

        df = ds.to_dataframe().reset_index()

        assert len(df) == nsteps

        expected_lons = np.linspace(start[0], end[0], nsteps)
        expected_lats = np.linspace(start[1], end[1], nsteps)

        assert np.allclose(sorted(df.lon.values), sorted(expected_lons))
        assert np.allclose(sorted(df.lat.values), sorted(expected_lats))

        assert np.isclose(df.lon.values[0], start[0])
        assert np.isclose(df.lat.values[0], start[1])
        assert np.isclose(df.lon.values[-1], end[0])
        assert np.isclose(df.lat.values[-1], end[1])

    def test_start_not_list(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(TypeError):
            ds.to_transect(start="a", end=[-20, 55], nsteps=10)
        assert len(nc.session_files()) == n

    def test_start_wrong_length(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(ValueError):
            ds.to_transect(start=[-70], end=[-20, 55], nsteps=10)
        assert len(nc.session_files()) == n

    def test_start_bad_element(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(TypeError):
            ds.to_transect(start=[-70, "a"], end=[-20, 55], nsteps=10)
        assert len(nc.session_files()) == n

    def test_end_missing(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(ValueError):
            ds.to_transect(start=[-70, 40], end=None, nsteps=10)
        assert len(nc.session_files()) == n

    def test_nsteps_missing(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(ValueError):
            ds.to_transect(start=[-70, 40], end=[-20, 55], nsteps=None)
        assert len(nc.session_files()) == n

    def test_nsteps_not_int(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(TypeError):
            ds.to_transect(start=[-70, 40], end=[-20, 55], nsteps=10.5)
        assert len(nc.session_files()) == n

    def test_nsteps_too_small(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(ValueError):
            ds.to_transect(start=[-70, 40], end=[-20, 55], nsteps=1)
        assert len(nc.session_files()) == n

    def test_invalid_method(self):
        ds = nc.open_data(ff, checks=False)
        n = len(nc.session_files())
        with pytest.raises(ValueError):
            ds.to_transect(start=[-70, 40], end=[-20, 55], nsteps=10, method="blah")
        assert len(nc.session_files()) == n
