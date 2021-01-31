import pandas as pd
import xarray as xr
import os, pytest

import importlib
import nctoolkit as nc

ff = "data/sst.mon.mean.nc"


class TestFinal:
    def test_a(self):

        assert len(nc.session.get_safe()) == 0
        assert len(nc.session.session_files()) == 0


