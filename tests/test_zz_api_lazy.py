import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


class TestApi(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_cores(self):
        nc.options(cores = 2)
        x = nc.session.session_info["cores"]
        self.assertEqual(x, 2)

    def test_cores_error(self):
        with self.assertRaises(TypeError) as context:
            nc.options(cores = 6.1)

    def test_no_data(self):

        with self.assertRaises(ValueError) as context:
            data = nc.open_data("")

    def test_no_data2(self):

        with self.assertRaises(ValueError) as context:
            data = nc.open_data()

    def test_no_files1(self):

        with self.assertRaises(TypeError) as context:
            data = nc.open_data([1,2])

    def test_options_setting(self):
        nc.options(precision = "F64")
        x = nc.session.session_info["precision"]
        self.assertEqual(x, "F64")

        nc.options(precision = "F32")


    def test_options_error(self):
        with self.assertRaises(ValueError) as context:
            nc.options(cores = 1000)

        with self.assertRaises(ValueError) as context:
            nc.options(precision = "I2")

    def test_empty_list(self):
        with self.assertRaises(ValueError) as context:
            x = nc.open_data([])

    def test_missing_file_list(self):
        with self.assertRaises(ValueError) as context:
            x = nc.open_data(["none.nc"])


    def test_simplifying(self):
        ff = "data/sst.mon.mean.nc"
        with self.assertWarns(Warning):
            data = nc.open_data([ff, ff])

    def test_options_invalid(self):
        with self.assertRaises(AttributeError) as context:
            nc.options(this = 1)

    def test_options_invalid2(self):
        with self.assertRaises(AttributeError) as context:
            nc.options(lazy = "x")

    def test_file_size(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.api.file_size(ff)
        self.assertEqual(x,  41073246)

    def test_open_data(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)
        self.assertEqual(x.current, "data/sst.mon.mean.nc")

    def test_merge(self):
        ff = "data/sst.mon.mean.nc"
        x = nc.open_data(ff)

        y = nc.open_data(ff)
        y.rename({"sst":"tos"})
        z = nc.merge(x,y)
        z.run()
        test = z.variables

        self.assertEqual(test, ["sst", "tos"])

    def test_size(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        x = "File size: 41.073246 MB" in data.size
        self.assertEqual(x, True)
        data.split("year")
        x = "Number of files in ensemble: 30" in data.size
        self.assertEqual(x, True)

    def test_repr(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        x = "operations: 0" in str(data)
        self.assertEqual(x, True)
        data.spatial_mean()
        x = "operations: 1" in str(data)
        self.assertEqual(x, True)

        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        x = "start: 60 member ensemble" in str(data)
        self.assertEqual(x, True)

    def test_variables_detailed(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        x = data.variables_detailed.query("variable == 'sst'").long_name.values
        self.assertEqual(x, "Monthly Means of Global Sea Surface Temperature")


    def test_cor_time(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        test = nc.cor_time(data, data)
        test.spatial_mean()
        x = test.to_dataframe().sst.values[0].astype("float")
        self.assertEqual(x, 1)
        data = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            test = nc.cor_time("y", data)
        with self.assertRaises(TypeError) as context:
            test = nc.cor_time(data,"y")

        data.split("year")
        with self.assertRaises(TypeError) as context:
            test = nc.cor_time(data,data)

    def test_delstart(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)

        with self.assertRaises(AttributeError) as context:
            del data.start

    def test_copy(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        files = data.current
        test = data.copy()
        del data

        x = len([ff for ff in nc.session.nc_safe if ff not in files])
        self.assertEqual(x, 0)

    def test_len(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        x = len(data)
        self.assertEqual(x, 60)
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        data.merge_time()
        data.run()
        x = len(data)
        self.assertEqual(x, 1)

    def test_getitem(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))
        x = data[0]
        self.assertEqual(x, data.current[0])

        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])
        x = data[0]
        self.assertEqual(x, data.current)

    def test_mergeerror(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble")[0])

        with self.assertRaises(TypeError) as context:
            test = nc.merge(data, "x")
    def test_opendatamissing(self):

        with self.assertRaises(ValueError) as context:
            data = nc.open_data(["nctoolkit/clip.py", "nctoolkit/regrid.py"], checks = True)




if __name__ == '__main__':
    unittest.main()

