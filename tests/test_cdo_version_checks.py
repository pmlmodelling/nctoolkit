import pytest

import nctoolkit as nc
from nctoolkit.session import session_info


@pytest.fixture
def cdo_version():
    orig = session_info["cdo"]
    yield
    session_info["cdo"] = orig


def test_spatial_percentile_blocked_on_cdo_261(cdo_version):
    session_info["cdo"] = "2.6.1"
    ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
    with pytest.raises(ValueError, match="downgrade CDO to version 2.4.1"):
        ds.spatial_percentile(50)
    # nothing was queued
    assert ds.history == []


def test_spatial_percentile_allowed_on_other_versions(cdo_version):
    session_info["cdo"] = "2.4.1"
    ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
    ds.spatial_percentile(50)
    assert any("fldpctl" in x for x in ds._hold_history + ds.history)


def test_other_methods_not_blocked_on_cdo_250(cdo_version):
    session_info["cdo"] = "2.5.0"
    ds = nc.open_data("data/woa18_decav_t01_01.nc", checks=False)
    ds.vertical_min()
    ds.vertical_max()
    ds.assign(new=lambda x: x.t_an - vertical_max(x.t_an))
    ds1 = nc.open_data("data/sst.mon.mean.nc", checks=False)
    ds1.spatial_percentile(50)


def test_vertical_max_allowed_on_other_versions(cdo_version):
    session_info["cdo"] = "2.4.1"
    ds = nc.open_data("data/woa18_decav_t01_01.nc", checks=False)
    ds.vertical_max()
    assert any("vertmax" in x for x in ds._hold_history + ds.history)
