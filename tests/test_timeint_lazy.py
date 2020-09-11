import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest
import subprocess


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"


class TestTimeint:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_timeint(self):
        # this test fails due to a bug in cdo 1.9.4. Ignore for now
        if cdo_version() not in ["1.9.4"]:
            tracker = nc.open_data(ff)
            tracker.time_interp(
                start="1990/01/01", end="1990/31/01", resolution="daily"
            )
            tracker.run()

            x = len(tracker.times)

            assert x == 365
            n = len(nc.session_files())
            assert n == 1

    def test_timeint1(self):
        if cdo_version() not in ["1.9.4"]:
            tracker = nc.open_data(ff)
            tracker.time_interp(
                start="1991/01/01", end="1991/31/01", resolution="weekly"
            )
            tracker.run()

            x = len(tracker.times)

            assert x == 53
            n = len(nc.session_files())
            assert n == 1

    def test_timeint2(self):
        if cdo_version() not in ["1.9.4"]:
            tracker = nc.open_data(ff)
            tracker.time_interp(
                start="1990/01/01", end="1990/31/01", resolution="monthly"
            )
            tracker.run()

            x = len(tracker.times)

            assert x == 12
            n = len(nc.session_files())
            assert n == 1

    def test_timeint3(self):
        if cdo_version() not in ["1.9.4"]:
            tracker = nc.open_data(ff)
            tracker.time_interp(
                start="1990/01/01", end="1993/01/01", resolution="yearly"
            )
            tracker.run()

            x = len(tracker.times)

            assert x == 4
            n = len(nc.session_files())
            assert n == 1

    def test_timeint4(self):
        tracker = nc.open_data(ff)
        tracker.time_interp(start="1990/01/01", resolution="yearly")
        tracker.run()

        x = len(tracker.times)

        assert x == 10
        n = len(nc.session_files())
        assert n == 1

    def test_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.time_interp(start="1990/01/01", end="1993/01/01", resolution="x")

        n = len(nc.session_files())
        assert n == 0

    def test_error2(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.time_interp(end="1993/01/01", resolution="daily")
        n = len(nc.session_files())
        assert n == 0

    def test_timeintstep(self):
        tracker = nc.open_data("data/2003.nc")
        x = len(tracker.times)

        tracker.timestep_interp(2)
        tracker.run()

        y = len(tracker.times)

        assert (x * 2 - 1) == y
