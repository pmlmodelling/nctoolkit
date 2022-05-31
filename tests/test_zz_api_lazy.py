import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


class TestApi:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_cores(self):
        nc.options(cores=2)
        x = nc.session.session_info["cores"]
        assert x == 2

    def test_cores_error(self):
        with pytest.raises(TypeError):
            nc.options(cores=6.1)

    def test_no_data(self):

        with pytest.raises(FileNotFoundError):
            data = nc.open_data("")

    def test_no_files1(self):

        with pytest.raises(TypeError):
            data = nc.open_data([1, 2])

    def test_options_setting(self):
        nc.options(precision="F64")
        x = nc.session.session_info["precision"]
        assert x == "F64"

        nc.options(precision="F32")

    def test_options_error(self):
        with pytest.raises(ValueError):
            nc.options(cores=1000)

        with pytest.raises(ValueError):
            nc.options(precision="I2")


    def test_missing_file_list(self):
        with pytest.raises(FileNotFoundError):
            x = nc.open_data(["none.nc"])

    def test_simplifying(self):
        ff = "data/sst.mon.mean.nc"
        with pytest.warns(UserWarning):
            data = nc.open_data([ff, ff])

    def test_options_invalid(self):
        with pytest.raises(AttributeError):
            nc.options(this=1)

    def test_options_invalid2(self):
        with pytest.raises(TypeError):
            nc.options(lazy="x")

    def test_file_size(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.api.file_size(ff)
        assert x == 41073246

    def test_open_data(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)
        assert x.current[0] == "data/sst.mon.mean.nc"

    def test_merge(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)

        y = nc.open_data(ff)
        y.rename({"sst": "tos"})
        z = nc.merge(x, y)
        z.run()
        test = z.variables

        assert test == ["sst", "tos"]

    def test_size(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        assert data.size["Ensemble size"] ==  "41.073246 MB" 
        data.split("year")
        assert data.size["Number of files in ensemble"] == 30

    def test_repr(self):

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        assert "Number of files: 60" in str(data)

    def test_contents(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        x = data.contents.query("variable == 'sst'").long_name.values
        assert x == "Monthly Means of Global Sea Surface Temperature"

    def test_cor_time(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        test = nc.cor_time(data, data)
        test.spatial_mean()
        x = test.to_dataframe().cor.values[0].astype("float")
        assert x == 1
        data = nc.open_data(ff)
        with pytest.raises(TypeError):
            test = nc.cor_time("y", data)
        with pytest.raises(TypeError):
            test = nc.cor_time(data, "y")

        data.split("year")
        with pytest.raises(TypeError):
            test = nc.cor_time(data, data)

    def test_delstart(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)

        with pytest.raises(AttributeError):
            del data.start

    def test_copy(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        files = data.current
        test = data.copy()
        del data

        x = len([ff for ff in nc.session.get_safe() if ff not in files])
        assert x == 0

    def test_len(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        x = len(data)
        assert x == 60
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge("time")
        data.run()
        x = len(data)
        assert x == 1

    def test_getitem(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        x = data[0]
        assert x == data.current[0]

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        x = data[0]
        assert x == data.current[0]

    def test_mergeerror(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])

        with pytest.raises(TypeError):
            test = nc.merge(data, "x")

    def test_opendatamissing(self):

        with pytest.raises(FileNotFoundError):
            data = nc.open_data(
                ["nctoolkit/clip.py", "nctoolkit/regrid.py"], checks=True
            )
