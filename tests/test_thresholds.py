import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/2003.nc"


class TestClip:
    def test_thresholds(self):

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds1.first_above(ds2)
        x = ds1.to_dataframe().analysed_sst.values[0]

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds2.run()
        ds1.first_above(ds2[0])
        y = ds1.to_dataframe().analysed_sst.values[0]

        assert x == y

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds1.last_above(ds2)
        x = ds1.to_dataframe().analysed_sst.values[0]

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds2.run()
        ds1.last_above(ds2[0])
        y = ds1.to_dataframe().analysed_sst.values[0]

        assert x == y

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds1.first_below(ds2)
        x = ds1.to_dataframe().analysed_sst.values[0]

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds2.run()
        ds1.first_below(ds2[0])
        y = ds1.to_dataframe().analysed_sst.values[0]

        assert x == y

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds1.last_below(ds2)
        x = ds1.to_dataframe().analysed_sst.values[0]

        ds1 = nc.open_data(ff)
        ds2 = nc.open_data(ff)
        ds2.tmean()
        ds2.run()
        ds1.last_below(ds2[0])
        y = ds1.to_dataframe().analysed_sst.values[0]

        assert x == y



        del ds1
        del ds2



        tracker = nc.open_data(ff)

        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.last_below(350)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 349

        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.first_above("x")
        with pytest.raises(ValueError):
            tracker.last_above("x")
        with pytest.raises(ValueError):
            tracker.first_below("x")
        with pytest.raises(ValueError):
            tracker.last_below("x")

        with pytest.raises(TypeError):
            tracker.first_above([])
        with pytest.raises(TypeError):
            tracker.last_above([])
        with pytest.raises(TypeError):
            tracker.first_below([])
        with pytest.raises(TypeError):
            tracker.last_below([])


        tracker = nc.open_data(ff)

        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        data = tracker.copy()
        data.subset(time = 350)
        data.run()

        tracker.last_below(data)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 349

        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.first_above(350)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0

        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        data = tracker.copy()
        data.subset(time = 349)
        tracker.first_above(data)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0



        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        tracker.run()
        print(tracker.variables)
        tracker.last_above(-351)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0

        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        data = tracker.copy()
        data.subset(time = 351)
        tracker.last_above(data)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 350.0



        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        tracker.first_below(-351)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 351.0




        tracker = nc.open_data(ff)
        if nc.utils.version_below(nc.session.session_info["cdo"], "2.1.0"):
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep(x.analysed_sst) + 0.01)
        else:
            tracker.assign(analysed_sst = lambda x: (x.analysed_sst == x.analysed_sst) * timestep() + 0.01)
        tracker.assign(analysed_sst = lambda x: -x.analysed_sst)
        data = tracker.copy()
        data.subset(time = 351)
        tracker.first_below(data)
        tracker.as_missing(0)
        tracker.spatial_mean()

        x = tracker.to_dataframe().analysed_sst.values[0]

        assert x == 352.0



