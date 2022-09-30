import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest, pytest


ff = "data/sst.mon.mean.nc"


class TestOverload:

    def test_overloading(self):

        ds = nc.open_data(ff)
        ds + 2000  
        assert ds.history[0] == "cdo -addc,2000"
        ds = nc.open_data(ff)
        ds + ds  
        assert ds.history[0] == 'cdo -add  infile09178 data/sst.mon.mean.nc'

        ds = nc.open_data(ff)
        ds - 2000  
        assert ds.history[0] == "cdo -subc,2000"
        ds = nc.open_data(ff)
        ds - ds  
        assert ds.history[0] == 'cdo -sub  infile09178 data/sst.mon.mean.nc'


        ds = nc.open_data(ff)
        ds * 2000  
        assert ds.history[0] == "cdo -mulc,2000"
        ds = nc.open_data(ff)
        ds * ds  
        assert ds.history[0] == 'cdo -mul  infile09178 data/sst.mon.mean.nc'


        ds = nc.open_data(ff)
        ds / 2000  
        assert ds.history[0] == "cdo -divc,2000"
        ds = nc.open_data(ff)
        ds / ds  
        assert ds.history[0] == 'cdo -div  infile09178 data/sst.mon.mean.nc'

        ds = nc.open_data(ff)
        ds ** 2000  
        assert ds.history[0] == "cdo -pow,2000"


        ds = nc.open_data(ff)
        ds / 2000  
        assert ds.history[0] == "cdo -divc,2000"
        ds = nc.open_data(ff)
        ds / ds  
        assert ds.history[0] == 'cdo -div  infile09178 data/sst.mon.mean.nc'

        ds = nc.open_data(ff)
        ds != 2
        assert ds.history[0] == 'cdo -nec,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds != ds
        assert "cdo -ne" in ds.history[1]

        ds = nc.open_data(ff)
        ds == 2
        assert ds.history[0] == 'cdo -eqc,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds == ds
        assert "cdo -eq" in ds.history[1]


        ds = nc.open_data(ff)
        ds > 2
        assert ds.history[0] == 'cdo -gtc,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds > ds
        assert "cdo -gt" in ds.history[1]


        ds = nc.open_data(ff)
        ds >= 2
        assert ds.history[0] == 'cdo -gec,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds >= ds
        assert "cdo -ge" in ds.history[1]

        ds = nc.open_data(ff)
        ds <= 2
        assert ds.history[0] == 'cdo -lec,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds <= ds
        assert "cdo -le" in ds.history[1]

        ds = nc.open_data(ff)
        ds < 2
        assert ds.history[0] == 'cdo -ltc,2'
        ds = nc.open_data(ff)
        ds.subset(time = 0)
        ds < ds
        assert "cdo -lt" in ds.history[1]





