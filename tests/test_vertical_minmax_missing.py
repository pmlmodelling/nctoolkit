import shutil

import netCDF4
import numpy as np
import pytest

import nctoolkit as nc

pytestmark = pytest.mark.skipif(shutil.which("cdo") is None, reason="cdo not available")

# CDO's vertmax and vertmin segfault for float32 variables that have grid cells
# missing at every level (e.g. land).
NLEV, NY, NX = 4, 6, 5

FILLS = {"f4": np.float32(9.96921e36), "f8": 9.96921e36, "i2": -32767, "i4": -999999}


def make_file(path, dtype, packed=False):
    rng = np.random.default_rng(1)
    values = rng.integers(-50, 100, (1, NLEV, NY, NX)).astype("f8")
    mask = np.zeros(values.shape, bool)
    mask[:, :, : NY // 2, :] = True  # missing at every level
    mask[:, NLEV // 2 :, NY // 2 :, : NX // 2] = True  # missing at some levels
    values = np.ma.masked_array(values, mask=mask)

    d = netCDF4.Dataset(path, "w")
    for name, size in [("time", None), ("depth", NLEV), ("lat", NY), ("lon", NX)]:
        d.createDimension(name, size)
    for name, units in [
        ("time", "days since 2000-01-01"),
        ("depth", "meters"),
        ("lat", "degrees_north"),
        ("lon", "degrees_east"),
    ]:
        d.createVariable(name, "f8", (name,)).units = units
    d["time"][:] = [0.0]
    d["depth"][:] = np.arange(NLEV)
    d["lat"][:] = np.arange(NY)
    d["lon"][:] = np.arange(NX)
    v = d.createVariable("t", dtype, ("time", "depth", "lat", "lon"), fill_value=FILLS[dtype])
    v[:] = values
    d.close()
    return values


@pytest.mark.parametrize("dtype", ["f4", "f8", "i2", "i4"])
@pytest.mark.parametrize("stat", ["max", "min"])
def test_vertical_stat_with_missing_columns(tmp_path, dtype, stat):
    path = str(tmp_path / "in.nc")
    values = make_file(path, dtype)
    ds = nc.open_data(path, checks=False)
    getattr(ds, f"vertical_{stat}")()
    ds.run()
    out = ds.to_xarray().t.values
    expected = getattr(values, stat)(axis=1)

    assert out.shape == (1, NY, NX)
    out = np.ma.masked_invalid(out.reshape(expected.shape).astype("f8"))
    # cells that are missing at every level stay missing
    assert (np.ma.getmaskarray(out) == np.ma.getmaskarray(expected)).all()
    assert np.allclose(out.compressed(), expected.compressed())
    assert len(nc.session_files()) == 1


def test_stand_in_values_are_valid_for_their_type():
    from nctoolkit.verticals import MISSING_STAND_IN, missing_stand_in

    limits = {"F32": np.finfo("f4").max, "F64": np.finfo("f8").max}
    limits.update({k: np.iinfo(v).max for k, v in {"I8": "i1", "I16": "i2", "I32": "i4"}.items()})
    for dtype, value in MISSING_STAND_IN.items():
        # plus and minus the value must both be storable
        assert value <= limits[dtype]
    # float32 with other types: the value is valid for all of them
    assert missing_stand_in(["F32"]) == 1e38
    assert missing_stand_in(["F32", "F64"]) == 1e38
    assert missing_stand_in(["F32", "I32"]) == 2147483647
    assert missing_stand_in(["F32", "I16", "I32"]) == 32767
    assert missing_stand_in(["F32", "I8"]) == 127
    # not needed without float32, and not possible with unsigned types
    assert missing_stand_in(["F64", "I16"]) is None
    assert missing_stand_in(["F32", "U8"]) is None


def test_mixed_types_with_missing_columns(tmp_path):
    # as in the WOA data: float32 variables plus 32 bit integer counts
    path = str(tmp_path / "mixed.nc")
    values = make_file(path, "f4")
    d = netCDF4.Dataset(path, "a")
    v = d.createVariable("n", "i4", ("time", "depth", "lat", "lon"), fill_value=-999999)
    counts = np.ma.masked_array(np.arange(NLEV * NY * NX).reshape(1, NLEV, NY, NX) % 7, mask=np.ma.getmaskarray(values))
    v[:] = counts
    d.close()

    for stat in ["max", "min"]:
        ds = nc.open_data(path, checks=False)
        getattr(ds, f"vertical_{stat}")()
        ds.run()
        for name, expected in [("t", getattr(values, stat)(axis=1)), ("n", getattr(counts, stat)(axis=1))]:
            out = np.ma.masked_invalid(ds.to_xarray()[name].values.astype("f8"))
            assert (np.ma.getmaskarray(out) == np.ma.getmaskarray(expected)).all()
            assert np.allclose(out.compressed(), expected.compressed())
