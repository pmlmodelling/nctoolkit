import shutil
import warnings

import numpy as np
import pytest
import xarray as xr

import nctoolkit as nc
from nctoolkit import session
from nctoolkit.session import replay_warnings

pytestmark = pytest.mark.skipif(shutil.which("cdo") is None, reason="cdo not available")

BOUNDS = "Grid cell bounds are not available"


@pytest.fixture(autouse=True)
def clean_queue():
    del session.session_warnings[:]
    cores = nc.session.session_info["cores"]
    yield
    nc.options(cores=cores)
    del session.session_warnings[:]


@pytest.fixture
def files(tmp_path):
    # a curvilinear grid with 2D lon/lat and no cell bounds: spatial_mean warns
    ny, nx = 20, 30
    y, x = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
    curv = xr.Dataset(
        {"sst": (("time", "y", "x"), np.ones((2, ny, nx), "f4"), {"coordinates": "nav_lon nav_lat"})},
        coords={
            "nav_lon": (("y", "x"), -10 + 0.3 * x + 0.05 * y),
            "nav_lat": (("y", "x"), 45 + 0.25 * y - 0.03 * x),
            "time": ("time", [0.0, 30.0], {"units": "days since 2013-01-01"}),
        },
    )
    regular = xr.Dataset(
        {"t": (("time", "lat", "lon"), np.ones((2, 4, 5), "f4"))},
        coords={
            "lat": ("lat", [50.0, 51, 52, 53], {"units": "degrees_north"}),
            "lon": ("lon", [-4.0, -3, -2, -1, 0], {"units": "degrees_east"}),
            "time": ("time", [0.0, 30.0], {"units": "days since 2013-01-01"}),
        },
    )
    out = dict(
        curv=str(tmp_path / "curv.nc"),
        curv2=str(tmp_path / "curv2.nc"),
        regular=str(tmp_path / "regular.nc"),
    )
    curv.to_netcdf(out["curv"])
    curv.to_netcdf(out["curv2"])
    regular.to_netcdf(out["regular"])
    return out


def spatial_mean_warnings(path):
    ds = nc.open_data(path, checks=False)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ds.spatial_mean()
        ds.run()
    return [str(x.message) for x in w]


def n_bounds(messages):
    return len([m for m in messages if BOUNDS in m])


def test_stale_warning_not_replayed(files):
    assert spatial_mean_warnings(files["regular"]) == []
    assert n_bounds(spatial_mean_warnings(files["curv"])) == 1
    assert len(session.session_warnings) == 0
    # cdo said nothing here, so nothing may be reported
    assert spatial_mean_warnings(files["regular"]) == []
    assert len(session.session_warnings) == 0


def test_warning_issued_on_each_occurrence(files):
    for _ in range(2):
        assert n_bounds(spatial_mean_warnings(files["curv"])) == 1
        assert len(session.session_warnings) == 0


def test_pool_warning_forwarded_once(files):
    nc.options(cores=2)
    ds = nc.open_data([files["curv"], files["curv2"]], checks=False)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ds.spatial_mean()
        ds.run()
    assert n_bounds([str(x.message) for x in w]) == 1
    assert len(session.session_warnings) == 0


def test_replay_drains_only_snapshot_and_dedupes():
    session.session_warnings.append((UserWarning, "a"))
    session.session_warnings.append((UserWarning, "a"))
    session.session_warnings.append((RuntimeWarning, "b"))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        replay_warnings()
    assert [(x.category, str(x.message)) for x in w] == [
        (UserWarning, "a"),
        (RuntimeWarning, "b"),
    ]
    assert len(session.session_warnings) == 0


def test_replay_keeps_warning_appended_during_replay():
    session.session_warnings.append((UserWarning, "a"))

    def append_late(*args, **kwargs):
        session.session_warnings.append((UserWarning, "late"))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        orig = warnings.showwarning
        warnings.showwarning = append_late
        try:
            warnings.simplefilter("always")
            replay_warnings()
        finally:
            warnings.showwarning = orig
    assert session.get_warnings() == [(UserWarning, "late")]
