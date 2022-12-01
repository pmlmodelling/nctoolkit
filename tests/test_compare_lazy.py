import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest


ff = "data/sst.mon.mean.nc"


class TestCompare:
    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0

    def test_compare(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare("<=0")
        tracker.run()
        tracker.spatial_sum()
        n = len(nc.session_files())
        assert n == 1

        x = tracker.to_dataframe().sst.values[0].astype("int")

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker<=0
        tracker.run()
        tracker.spatial_sum()
        n = len(nc.session_files())
        assert n == 1

        x = tracker.to_dataframe().sst.values[0].astype("int")

    def test_compare_error(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.compare("==")
        with pytest.raises(ValueError):
            tracker.compare("<=")
        with pytest.raises(ValueError):
            tracker.compare(">=")

        with pytest.raises(ValueError):
            tracker.compare(">")
        with pytest.raises(ValueError):
            tracker.compare("<")
        with pytest.raises(ValueError):
            tracker.compare("")
        with pytest.raises(ValueError):
            tracker.compare("!=")

        with pytest.raises(ValueError):
            tracker.compare()

        with pytest.raises(TypeError):
            tracker.compare(1)

        n = len(nc.session_files())

        assert n == 0

    def test_compare1(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker-1
        tracker<-1
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 9356

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker<0
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 9356
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare("<0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 9356

        n = len(nc.session_files())
        assert n == 1

    def test_compare2(self):

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker-1
        tracker>-1
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")
        assert x == 34441

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker>0
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")
        assert x == 34441

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare(">0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")
        assert x == 34441

        n = len(nc.session_files())
        assert n == 1

    def test_compare3(self):

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker-1
        tracker==-1
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 2

        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker==0
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 2
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare("==0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 2
        n = len(nc.session_files())
        assert n == 1

    def test_compare4(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker!=0
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 43797
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare("!=0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 43797
        n = len(nc.session_files())
        assert n == 1

    def test_compare5(self):
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker>=0
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 34443
        tracker = nc.open_data(ff)
        tracker.subset(years=list(range(1970, 1971)))
        tracker.subset(months=[1])
        tracker.compare(">=0")
        tracker.run()
        tracker.spatial_sum()

        x = tracker.to_dataframe().sst.values[0].astype("int")

        assert x == 34443
        n = len(nc.session_files())
        assert n == 1
