import nctoolkit as nc
import subprocess
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"


class TestClip:
    def test_merid1(self):
        ds = nc.open_data("data/vertical_tester.nc")
        with pytest.raises(TypeError):
            ds.meridonial_mean()
        tracker = nc.open_data(ff, checks = False)
        n = len(nc.session_files())
        assert n == 0

        tracker = nc.open_data(ff, checks = False)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.meridonial_mean()
        data.spatial_mean()
        if cdo_version() not in ["1.9.3", "1.9.4"]:
            assert data.to_dataframe().sst[0].astype("float") == 15.605058670043945 
        else:
            assert data.to_dataframe().sst[0].astype("float") == 17.679880142211914

        tracker = nc.open_data(ff, checks = False)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.meridonial_min()
        data.spatial_mean()
        if cdo_version() not in ["1.9.3", "1.9.4"]:
            assert (data.to_dataframe().sst[0].astype("float") == 6.8090081214904785)
        else:
            assert (data.to_dataframe().sst[0].astype("float") == -1.7714282274246216)

        tracker = nc.open_data(ff, checks = False)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.meridonial_max()
        data.spatial_mean()
        if cdo_version() not in ["1.9.3", "1.9.4"]:
            assert data.to_dataframe().sst[0].astype("float") == 21.77419662475586  
        else:
            assert data.to_dataframe().sst[0].astype("float") == 27.9967041015625

        tracker = nc.open_data(ff, checks = False)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.meridonial_range()
        data.spatial_mean()
        if cdo_version() not in ["1.9.3", "1.9.4"]:
            assert data.to_dataframe().sst[0].astype("float") == 14.965188026428223 
        else:
            assert data.to_dataframe().sst[0].astype("float") == 29.76813316345215
        del data
        del tracker
        del ds

        n = len(nc.session_files())
        assert n == 0
        assert len(nc.session.get_safe()) == 0