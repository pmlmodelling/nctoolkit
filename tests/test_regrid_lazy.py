import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestRegrid(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_regrid(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        tracker.regrid(new, method = "nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)

        n = len(nc.session_files())
        self.assertEqual(n, 2)


    def test_regrid_list(self):
        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        new = tracker.copy()
        tracker.select_months(1)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select_years(1990)
        tracker.select_months(1)
        new.split("yearmonth")
        tracker.regrid(new, method = "nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 1 + 12)

    def test_invalid_method(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.regrid(tracker, method = "x")
        n = len(nc.session_files())
        self.assertEqual(n, 0)


    def test_error11(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.regrid(grid = 1)
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error1(self):
        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker.regrid("/tmp/stekancihwn.nc")
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_error2(self):
        tracker = nc.open_data(ff)
        from pathlib import Path
        import os
        out = nc.temp_file.temp_file()
        Path(out).touch()
        with self.assertRaises(ValueError) as context:
            tracker.regrid(out)
        #os.remove(out)
        n = len(nc.session_files())
        self.assertEqual(n, 0)



    def test_montherror(self):
        tracker = nc.open_data(ff)
        tracker.run()
        with self.assertRaises(ValueError) as context:
            tracker.regrid()

        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_regrid1(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        grid = new.to_dataframe().reset_index().loc[:,["lon", "lat"]]

        tracker = nc.open_data(ff)
        tracker.select_timestep(1)
        tracker.regrid(grid, method = "nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        self.assertEqual(x, y)
        n = len(nc.session_files())
        self.assertEqual(n, 2)


    def test_single(self):

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5], "lat":[55.5]})
        data.regrid(grid)
        x = data.to_dataframe().sst.values[0]


        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5], "lat":[55.5]})
        data.clip(lon = [1.2, 1.7], lat = [55.2, 55.7])
        y = data.to_dataframe().sst.values[0]

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_another_df(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5, 1.5], "lat":[55.5, 56.5]})
        data.regrid(grid)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0]

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5], "lat":[55.5]})
        data.clip(lon = [1.2, 1.7], lat = [55.2, 56.7])
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0]
        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_another_df2(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5, 2.5], "lat":[55.5, 55.5]})
        data.regrid(grid)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0]

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        data.clip(lon = [1.2, 2.7], lat = [55.2, 55.7])
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0]
        self.assertEqual(x,y)
        ff = "data/sst.mon.mean.nc"
        n = len(nc.session_files())
        self.assertEqual(n, 1)

    def test_another_df3(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5, 1.5, 20], "lat":[55.5, 56.5, 56.5]})
        data.regrid(grid, "nn")
        data.clip(lon = [0, 2])
        x = data.to_dataframe().sst.mean()

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select_timestep(0)
        grid = pd.DataFrame({"lon":[1.5], "lat":[55.5]})
        data.clip(lon = [1.2, 1.7], lat = [55.2, 56.7])
        y = data.to_dataframe().sst.mean()

        self.assertEqual(x,y)
        n = len(nc.session_files())
        self.assertEqual(n, 1)

if __name__ == '__main__':
    unittest.main()

