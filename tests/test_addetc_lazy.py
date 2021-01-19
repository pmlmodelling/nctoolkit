import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import numpy as np
import os, pytest, pytest


ff = "data/sst.mon.mean.nc"


class TestAddetc:
    def test_merger(self):
        new = nc.open_data(ff)
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.merge_time()
        tracker.subtract(new)
        tracker.tmean()
        x = tracker.to_dataframe().sst.values[0]

        assert x == 0

        n = len(nc.session_files())
        assert n == 1

    def test_add_safe(self):
        nc.options(lazy = False)
        tracker = nc.open_data(ff)
        tracker.select(years = list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.multiply(2)
        tracker.spatial_mean()
        new.add(new)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x  == y

        n = len(nc.session_files())
        assert n == 2
        nc.options(lazy = True)

    def test_add(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.spatial_mean()
        new.add(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x + 1 == y

        n = len(nc.session_files())
        assert n == 2

    def test_add_multiple(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker)
        new.subtract(tracker)
        new.subtract(tracker)
        new.spatial_mean()

        x = new.to_dataframe().sst.values[0]

        assert x == 0

        n = len(nc.session_files())
        assert n == 2

    def test_add2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]

        y = new.to_dataframe().sst.values[0]

        assert x + x == y
        n = len(nc.session_files())
        assert n == 2

    def test_add21(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker, "sst")
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x + x == y

        n = len(nc.session_files())
        assert n == 2

    def test_add_var(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.mutate({"tos": "sst+1-1"})
        tracker.run()
        new.add(tracker, var="tos")
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x + x == y
        n = len(nc.session_files())
        assert n == 2

    def test_add3(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker.current)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x + x == y

        n = len(nc.session_files())
        assert n == 2

    def test_add4(self):
        nc.options(lazy=False)
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker.current)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert x + x == y

        n = len(nc.session_files())
        assert n == 2
        nc.options(lazy=True)

    def test_subtract(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(1)
        new.subtract(tracker)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert y == 1
        n = len(nc.session_files())
        assert n == 2

    def test_subtract1(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(1)
        new.subtract(tracker.current)
        new.spatial_mean()
        tracker.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = new.to_dataframe().sst.values[0]

        assert y == 1
        n = len(nc.session_files())
        assert n == 2

    def test_op_list(self):
        ff = "data/sst.mon.mean.nc"
        data = nc.open_data(ff)
        data.select(timesteps=0)
        new = nc.open_data(ff)
        new.select(timesteps=[0, 1])
        new.split("yearmonth")
        new.subtract(data)
        new.merge_time()
        new.select(timesteps=0)
        new.spatial_sum()
        x = new.to_dataframe().sst.values[0].astype("float")

        assert x == 0.0
        n = len(nc.session_files())
        assert n == 2

    def test_subtract2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.spatial_mean()
        new.subtract(1)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        assert x - 1 == y
        n = len(nc.session_files())
        assert n == 2

    def test_multiply(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.spatial_mean()
        new.multiply(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        assert np.round(x * 10, 4).astype("float") == np.round(y, 4).astype("float")
        n = len(nc.session_files())
        assert n == 2

    def test_multiply1(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.multiply(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        assert x == y * 2
        n = len(nc.session_files())
        assert n == 3

    def test_multiply2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker.current)
        out = tracker.copy()
        tracker.multiply(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        assert x == y * 2
        n = len(nc.session_files())
        assert n == 3

    def test_divide(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        tracker.spatial_mean()
        new.divide(10)
        new.spatial_mean()

        x = tracker.to_dataframe().sst.values[0].astype("float")
        y = new.to_dataframe().sst.values[0].astype("float")

        assert np.round(x / 10, 4) == np.round(y, 4)
        n = len(nc.session_files())
        assert n == 2

    def test_divide1(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        assert x == y / 2
        n = len(nc.session_files())
        assert n == 3

    def test_divide2(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker.current)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        assert x == y / 2
        n = len(nc.session_files())
        assert n == 3

    def test_divide3(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(2)
        new.subtract(tracker.current)
        out = tracker.copy()
        tracker.divide(new)
        tracker.spatial_mean()
        out.spatial_mean()

        x = tracker.to_dataframe().sst.values[0]
        y = out.to_dataframe().sst.values[0]

        assert x == y / 2
        n = len(nc.session_files())
        assert n == 3

    def test_file_incompat(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        data2 = nc.open_data(ff2)
        data2.mutate({"tos": "analysed_sst + 2"})
        data2.run()
        # with pytest.raises(ValueError):
        with pytest.raises(ValueError):
            tracker.add(data2.current)
        n = len(nc.session_files())
        assert n == 1

    def test_file_incompat1(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        data2 = nc.open_data(ff2)
        data2.mutate({"tos": "analysed_sst + 2"})
        data2.run()
        with pytest.raises(ValueError):
            tracker.subtract(data2)
        n = len(nc.session_files())
        assert n == 1

    def test_file_incompat2(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        data2 = nc.open_data(ff2)
        data2.mutate({"tos": "analysed_sst + 2"})
        data2.run()
        with pytest.raises(ValueError):
            tracker.divide(data2)
        n = len(nc.session_files())
        assert n == 1

    def test_file_incompat3(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.multiply("xyz")
        n = len(nc.session_files())
        assert n == 0

    def test_file_incompat4(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.subtract("xyz")
        n = len(nc.session_files())
        assert n == 0

    def test_file_incompat5(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.add("xyz")
        n = len(nc.session_files())
        assert n == 0

    def test_file_incompat6(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.divide("xyz")
        n = len(nc.session_files())
        assert n == 0

    def test_file_incompat7(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        data2 = nc.open_data(ff2)
        data2.mutate({"tos": "analysed_sst+2"})
        data2.run()
        with pytest.raises(ValueError):
            tracker.multiply(data2)
        n = len(nc.session_files())
        assert n == 1

    def test_file_typeerror(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with pytest.raises(TypeError):
            tracker.multiply([1, 2])
        n = len(nc.session_files())
        assert n == 0

    def test_file_typeerror1(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with pytest.raises(TypeError):
            tracker.subtract([1, 2])
        n = len(nc.session_files())
        assert n == 0

    def test_file_typeerror2(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with pytest.raises(TypeError):
            tracker.add([1, 2])

        n = len(nc.session_files())
        assert n == 0

    def test_file_typeerror3(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with pytest.raises(TypeError):
            tracker.divide([1, 2])
        n = len(nc.session_files())
        assert n == 0

    def test_file_typeerror4(self):
        tracker = nc.open_data(ff)
        ff2 = "data/2003.nc"
        with pytest.raises(TypeError):
            tracker.divide([1, 2])
        n = len(nc.session_files())
        assert n == 0

    def test_var_typeerror(self):
        tracker = nc.open_data(ff)
        with pytest.raises(TypeError):
            tracker.add(tracker, var=1)

    def test_var_valueerror(self):
        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker.add(tracker, var="tos222")

    def test_lazy_add(self):
        tracker = nc.open_data(ff)
        tracker.select(years=list(range(1970, 1971)))
        tracker.select(months=[1])
        tracker.run()
        new = tracker.copy()
        new.add(tracker, "sst")
        new.subtract(tracker, "sst")
        new.subtract(tracker, "sst")
        new.spatial_mean()

        x = new.to_dataframe().sst.values[0]

        assert x == 0

        n = len(nc.session_files())
        assert n == 2

    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0
