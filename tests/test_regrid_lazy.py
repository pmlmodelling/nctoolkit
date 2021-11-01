import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestRegrid:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0
    def test_list(self):

        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.to_latlon(lon = [-90, 90], lat = [0, 40], res = 1)
        tracker.merge_time()
        tracker.tmean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.to_latlon(lon = [-90, 90], lat = [0, 40], res = 1)
        tracker.tmean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")


        assert x == y

        tracker = nc.open_data(ff)
        tracker.select(year = 1990)
        tracker.split("month")
        tracker.to_latlon(lon = [-90, 90], lat = [0, 40], res = 1)
        assert len(tracker) == 12
        tracker.merge_time()
        tracker.tmean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select(year = 1990)
        tracker.to_latlon(lon = [-90, 90], lat = [0, 40], res = 1)
        tracker.tmean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")


        assert x == y


    def test_regrid(self):
        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        tracker.select(months=1)
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        tracker.select(months=1)
        tracker.regrid(new, method="nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y

        n = len(nc.session_files())
        assert n == 2

    def test_regrid_list(self):
        tracker = nc.open_data(ff)
        tracker.select(years=1990)
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        new = tracker.copy()
        tracker.select(months=1)
        tracker.regrid(new)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data(ff)
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        tracker.select(years=1990)
        tracker.split("yearmonth")
        tracker.regrid(new)
        tracker.merge_time()
        tracker.select(months=1)
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y

        n = len(nc.session_files())
        assert n == 2

        tracker = nc.open_data(ff)
        tracker.split("year")
        new = nc.open_data(ff)
        with pytest.warns(UserWarning):
            new.regrid(tracker)

    def test_invalid_method(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.regrid(tracker, method="x")
        n = len(nc.session_files())
        assert n == 0

    def test_error11(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.regrid(grid=1)

        tracker = nc.open_data("data/20*.nc")
        with pytest.raises(ValueError):
            tracker.regrid(grid=ff, recycle = True)

        with pytest.raises(ValueError):
            tracker.regrid(grid=pd.DataFrame())

        n = len(nc.session_files())
        assert n == 0
        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.regrid(grid=1)




    def test_error1(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.regrid("/tmp/stekancihwn.nc")
        n = len(nc.session_files())
        assert n == 0
    def test_1(self):
        assert 1 == 1

    def test_error2(self):
        tracker = nc.open_data(ff)
        from pathlib import Path
        import os, pytest

        out = nc.temp_file.temp_file()
        Path(out).touch()
        with pytest.raises(ValueError):
            tracker.regrid(out)
        with pytest.raises(ValueError):
            tracker.regrid(out)
        n = len(nc.session_files())
        assert n == 0

    def test_montherror(self):
        tracker = nc.open_data(ff)
        tracker.run()
        with pytest.raises(ValueError):
            tracker.regrid()

        n = len(nc.session_files())
        assert n == 0

    def test_regrid1(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.crop(lon=[0, 90])
        tracker.crop(lat=[0, 90])
        new = tracker.copy()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        grid = new.to_dataframe().reset_index().loc[:, ["lon", "lat"]]

        tracker = nc.open_data(ff)
        tracker.select(timesteps=1)
        tracker.regrid(grid, method="nn")
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0].astype("float")

        assert x == y
        n = len(nc.session_files())
        assert n == 2

    def test_single(self):

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5], "lat": [55.5]})
        data.regrid(grid)
        x = data.to_dataframe().sst.values[0]

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5], "lat": [55.5]})
        data.crop(lon=[1.2, 1.7], lat=[55.2, 55.7])
        y = data.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_another_df(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5, 1.5], "lat": [55.5, 56.5]})
        data.regrid(grid)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0]

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5], "lat": [55.5]})
        data.crop(lon=[1.2, 1.7], lat=[55.2, 56.7])
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0]
        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_another_df2(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5, 2.5], "lat": [55.5, 55.5]})
        data.regrid(grid)
        data.spatial_mean()
        x = data.to_dataframe().sst.values[0]

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        data.crop(lon=[1.2, 2.7], lat=[55.2, 55.7])
        data.spatial_mean()
        y = data.to_dataframe().sst.values[0]
        assert x == y
        ff = "data/sst.mon.mean.nc"
        n = len(nc.session_files())
        assert n == 1

    def test_another_df3(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5, 1.5, 20], "lat": [55.5, 56.5, 56.5]})
        data.regrid(grid, "nn")
        data.crop(lon=[0, 2])
        x = data.to_dataframe().sst.mean()

        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        grid = pd.DataFrame({"lon": [1.5], "lat": [55.5]})
        data.crop(lon=[1.2, 1.7], lat=[55.2, 56.7])
        y = data.to_dataframe().sst.mean()

        assert x == y
        n = len(nc.session_files())
        assert n == 1
