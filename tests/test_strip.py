import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


import subprocess



class TestSetters:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

        ds = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds.top()
        ds.subset(time = 0)
        ds.spatial_mean()
        df1 = ds.to_dataframe()
        ds.strip_variables()
        assert 'ncks -C -v t_an,t_dd,t_gp,t_ma,t_mn,t_oa,t_sd,t_se' in ds.history[1]
        df2 = ds.to_dataframe()
        assert len([x for x in df1.columns if "bnds" in x]) > 0
        assert len([x for x in df2.columns if "bnds" in x]) == 0



        ds = nc.open_data("data/woa18_decav_t01_01.nc", checks = False)
        ds.top()
        ds.subset(time = 0)
        ds.spatial_mean()
        df1 = ds.to_dataframe()
        ds.strip_variables("t_an")
        df2 = ds.to_dataframe()
        assert len([x for x in df1.columns if "bnds" in x]) > 0
        assert len([x for x in df2.columns if "bnds" in x]) == 0
        assert ds.variables == ["t_an"]

        # valueerror check

        with pytest.raises(ValueError):
            ds.strip_variables("asdf")
