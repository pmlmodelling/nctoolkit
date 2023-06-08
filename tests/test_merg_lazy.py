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
        with pytest.warns(UserWarning):
            tracker.collect()
        tracker.run()
        n = len(nc.session_files())
        assert n == 0

        ds1 = nc.open_data("data/200*.nc")
        ds1.subset(lon = [-15, -13], lat = [50, 52])
        ds1.split("month")
        ds1.split("day")
        assert len(ds1) == 731
        ds1.merge("time")
        ds1.run()
        ds1.merge("time")
        
        assert len(ds1.times) == 731

    def test_warning1(self):
        tracker = nc.open_data(ff)

        with pytest.warns(UserWarning):
            tracker.merge("time")
        tracker.run()
        n = len(nc.session_files())
        assert n == 0

    def test_warning2(self):
        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0, 1, 2])
        tracker.run()
        new = nc.open_data(ff)
        new.subset(timesteps=[0])
        new.rename({"sst": "tos"})
        new.run()
        data = nc.open_data([tracker.current[0], new.current[0]])
        with pytest.warns(UserWarning):
            data.merge(match="year")

        data.run()

        n = len(nc.session_files())
        assert n == 3

    def test_merge_time(self):


        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge("time")
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
        tracker.subset(timesteps=[0, 1, 2])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.subset(timesteps=112)
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


        with pytest.raises(ValueError):
            ds = nc.open_data(["data/sst.mon.mean.nc", "data/2003.nc"] )
            ds.merge("time")

    def test_merge_error1(self):
        tracker = nc.open_data(ff)
        tracker.subset(timesteps=[0])
        tracker.run()
        new = tracker.copy()

        new = nc.open_data(ff)
        new.subset(timesteps=[0, 1, 2])
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


    def test_collect(self):
        tracker = nc.open_data(ff)
        tracker.subset(time =0)
        tracker.distribute(4,4)
        tracker.collect()
        tracker.spatial_sum()
        x = tracker.to_dataframe().sst.values[0]

        tracker = nc.open_data(ff)
        tracker.subset(time =0)
        tracker.distribute(4,4)
        tracker.collect()
        tracker.spatial_sum()
        y = tracker.to_dataframe().sst.values[0]

        assert x == y


    def test_merge_error4(self):
        tracker = nc.open_data(ff)
        tracker.run()
        new = tracker.copy()
        new.rename({"sst": "tos"})
        new.subset(timesteps=[1, 2, 3, 4])
        tracker.subset(timesteps=[0, 2, 3, 4])
        tracker.run()
        new.run()

        data = nc.open_data([new.current[0], tracker.current[0]])

        with pytest.raises(ValueError):
            data.merge()
        n = len(nc.session_files())
        assert n == 2
