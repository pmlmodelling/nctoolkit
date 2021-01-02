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
    def test_zonal1(self):
        tracker = nc.open_data(ff)
        n = len(nc.session_files())
        assert n == 0

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.zonal_mean()
        data.spatial_mean()
        if cdo_version() != "1.9.3":
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 17.550573348999023
            )
        else:
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 17.550796508789062
            )

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.zonal_min()
        data.spatial_mean()
        if cdo_version() != "1.9.3":
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 13.19449520111084
            )
        else:
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 13.19469928741455
            )

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.zonal_max()
        data.spatial_mean()
        if cdo_version() != "1.9.3":
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 20.55069923400879
            )
        else:
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 20.55091094970703
            )

        tracker = nc.open_data(ff)
        data = nc.open_data("data/sst.mon.mean.nc")
        data.tmean()
        data.zonal_range()
        data.spatial_mean()
        if cdo_version() != "1.9.3":
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 7.356204986572266
            )
        else:
            assert (
                data.to_dataframe().sst[0].values[0].astype("float")
                == 7.345167636871338
            )
