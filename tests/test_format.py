import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestFormat:

    def test_format(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        assert data.ncformat == ['NetCDF4 classic zip']

        data = nc.open_data(ff)
        data.format("nc2")
        data.run()

        assert data.ncformat == ["NetCDF2"]


        data = nc.open_data(ff)

        nc.options(lazy = False)
        data = nc.open_data(ff)
        data.format("nc2")
        data.run()

        assert data.ncformat == ["NetCDF2"]
        nc.options(lazy = True)

        with pytest.raises(ValueError):
            data.format("nc123")
        with pytest.raises(TypeError):
            data.format(1 )

        with pytest.raises(ValueError):
            data.format( )
