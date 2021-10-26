import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)

ff = "data/sst.mon.mean.nc"


class TestMerge:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_warning(self):
        tracker = nc.open_data(ff)

        with pytest.warns(UserWarning):
            tracker.merge()
        tracker.run()
        n = len(nc.session_files())
        assert n == 0

    def test_warning1(self):
        tracker = nc.open_data(ff)

        with pytest.warns(UserWarning):
            tracker.merge_time()
        tracker.run()
        n = len(nc.session_files())
        assert n == 0

    def test_warning2(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0, 1, 2])
        tracker.run()
        new = nc.open_data(ff)
        new.select(timesteps=[0])
        new.rename({"sst": "tos"})
        new.run()
        data = nc.open_data([tracker.current[0], new.current[0]])
        with pytest.warns(UserWarning):
            data.merge(match="year")

        data.run()

        n = len(nc.session_files())
        assert n == 3

    def test_merge_time(self):


        ds1 = nc.open_data("data/2003.nc")
        ds2 = nc.open_data("data/2004.nc")
        ds2.assign(sst = lambda x: x.analysed_sst - 273.15)
        ds1.append(ds2)
        ds1.merge_time()
        ds1.tmean()
        ds1.spatial_mean()
        x = ds1.to_dataframe().analysed_sst.values[0]

        ds1 = nc.open_data("data/2003.nc")
        ds2 = nc.open_data("data/2004.nc")
        ds1.append(ds2)
        ds1.merge_time()
        ds1.tmean()
        ds1.spatial_mean()

        y = ds1.to_dataframe().analysed_sst.values[0]


        assert x == y

        del ds1
        del ds2


        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.tmean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge(join = "time")
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.tmean()
        tracker.spatial_mean()

        y = tracker.to_dataframe().sst.values[0]

        assert x == y
        n = len(nc.session_files())
        assert n == 1

    def test_merge(self):
        tracker = nc.open_data(ff)
        tracker.run()
        new = tracker.copy()
        new.rename({"sst": "tos"})
        new.run()
        data = nc.open_data([new.current[0], tracker.current[0]])
        data.merge()
        data.assign(test1 = lambda x:  x.tos-x.sst)
        data.spatial_mean()
        x = data.to_dataframe().test1.values[0]
        assert x == 0
        n = len(nc.session_files())
        assert n == 2

    def test_merge_error(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0, 1, 2])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select(timesteps=112)
        new.run()
        new.rename({"sst": "tos"})
        new.run()
        data = nc.open_data([new.current[0], tracker.current[0]])
        with pytest.raises(ValueError):
            data.merge()

        n = len(nc.session_files())
        assert n == 2

        data = nc.open_data([new.current[0], tracker.current[0]])
        with pytest.raises(TypeError):
            data.merge(match=1)

    def test_merge_error1(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select(timesteps=[0, 1, 2])
        new.run()
        new.rename({"sst": "tos"})
        new.run()
        data = nc.open_data([tracker.current[0], new.current[0]])
        with pytest.raises(ValueError):
            data.merge(match="month")

        with pytest.raises(TypeError):
            data.merge(match=[1])

        with pytest.raises(ValueError):
            data.merge(match="test")

        with pytest.raises(ValueError):
            data.merge()

        n = len(nc.session_files())

        tracker = nc.open_data(ff)

    def test_merge_error2(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0, 1, 2])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select(timesteps=112)
        new.run()
        new.rename({"sst": "tos"})
        new.crop(lon=[50, 80])
        new.run()
        data = nc.open_data([new.current[0], tracker.current[0]])
        with pytest.raises(ValueError):
            data.merge(match="year")
        n = len(nc.session_files())
        assert n == 2

    def test_merge_error3(self):
        tracker = nc.open_data(ff)
        tracker.select(timesteps=[0, 1])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.select(timesteps=[3, 4])
        new.run()
        new.rename({"sst": "tos"})
        new.crop(lon=[50, 80])
        new.run()
        data = nc.open_data([new.current[0], tracker.current[0]])
        with pytest.raises(ValueError):
            data.merge(match=["year", "month"])
        n = len(nc.session_files())
        assert n == 2

    def test_merge_error4(self):
        tracker = nc.open_data(ff)
        tracker.run()
        new = tracker.copy()
        new.rename({"sst": "tos"})
        new.select(timesteps=[1, 2, 3, 4])
        tracker.select(timesteps=[0, 2, 3, 4])
        tracker.run()
        new.run()

        data = nc.open_data([new.current[0], tracker.current[0]])

        with pytest.raises(ValueError):
            data.merge()
        n = len(nc.session_files())
        assert n == 2
