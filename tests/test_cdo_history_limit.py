import shutil

import numpy as np
import pytest
import xarray as xr

import nctoolkit as nc

pytestmark = pytest.mark.skipif(shutil.which("cdo") is None, reason="cdo not available")

# CDO 2.6.5 fails when writing a history attribute of more than about 32 KB.
# That happens when many files with long names are merged, as the merge command
# is appended to the history. Neither the length of the inputs' history nor the
# number of files is a problem on their own.
N_FILES = 80
NAME_LENGTH = 200
HISTORY = "Wed Oct 30 08:44:00 2019: cdo -sellonlatbox,-22,37,10,66 in.nc out.nc\n" * 300


@pytest.fixture
def files(tmp_path):
    out = []
    for i in range(N_FILES):
        ds = xr.Dataset(
            {"t": (("time", "lat", "lon"), np.full((1, 3, 4), float(i), "f4"))},
            coords={
                "time": ("time", [float(i)], {"units": "days since 2000-01-01"}),
                "lat": ("lat", [1.0, 2, 3], {"units": "degrees_north"}),
                "lon": ("lon", [1.0, 2, 3, 4], {"units": "degrees_east"}),
            },
            attrs={"history": HISTORY},
        )
        path = tmp_path / (f"f{i:03d}_".ljust(NAME_LENGTH - 3, "x") + ".nc")
        ds.to_netcdf(path)
        out.append(str(path))
    return out


def test_merge_with_very_long_history(files):
    ds = nc.open_data(files, checks=False)
    ds.merge("time")
    ds.run()
    assert len(ds.times) == N_FILES
    # only the merged file may be left
    assert len(nc.session_files()) == 1
    ds.spatial_mean()
    ds.run()
    assert ds.to_xarray().t.values.ravel().tolist() == [
        float(i) for i in range(N_FILES)
    ]
