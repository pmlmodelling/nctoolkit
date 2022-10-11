import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import warnings


class TestVerts:


    def test_integration(self):

        ds1 = nc.open_data("data/woa18_decav_t01_01.nc")
        ds1.subset(variable = "t_an")
        ds1.vertical_integration(depth_range = [0, 2.0])
        ds2 = nc.open_data("data/woa18_decav_t01_01.nc")
        ds2.subset(variable = "t_an")
        ds2.top()
        ds1.divide(ds2)
        ds1.spatial_mean()
        assert ds1.to_dataframe().t_an.values[0] == 2.0

        ff = "data/vertical_tester.nc"

        ff = "data/vertical_tester.nc"

        ds = nc.open_data(ff)


        with pytest.raises(TypeError):
            ds.vertical_integration("e3t", depth_range = 1)

        with pytest.raises(ValueError):
            ds.vertical_integration("e3t", depth_range = [1,2,3])

        with pytest.raises(ValueError):
            ds.vertical_integration("e3t", depth_range = [30,20])

        with pytest.raises(TypeError):
            ds.vertical_mean("e3t", depth_range = 1)

        with pytest.raises(ValueError):
            ds.vertical_mean("e3t", depth_range = [1,2,3])

        with pytest.raises(ValueError):
            ds.vertical_mean("e3t", depth_range = [30,20])

        with pytest.raises(ValueError):
            ds.vertical_mean(thickness = 1)

        with pytest.raises(ValueError):
            ds.vertical_integration(thickness = 1)

        with pytest.raises(ValueError):
            ds.vertical_integration(thickness = ff)

        with pytest.raises(ValueError):
            ds.vertical_mean(thickness = ff)

        with pytest.raises(ValueError):
            ds1 = nc.open_data(ff)
            ds.vertical_mean(thickness = ds1)

        with pytest.raises(ValueError):
            ds1 = nc.open_data(ff)
            ds.vertical_integration(thickness = ds1)

        ds = nc.open_data("data/vertical_tester.nc")
        ds.vertical_mean("e3t", depth_range = [0, 30])
        ds.spatial_sum()
        x = ds.to_dataframe().one.sum()

        ds = nc.open_data("data/vertical_tester.nc")
        ds1 = nc.open_data("data/vertical_tester.nc")
        ds1.subset(variables = "e3t")
        ds.vertical_mean(ds1, depth_range = [0,30])
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y


        ds = nc.open_data("data/vertical_tester.nc")
        ds.vertical_mean("e3t")
        ds.spatial_sum()
        x = ds.to_dataframe().one.sum()

        ds = nc.open_data("data/vertical_tester.nc")
        ds1 = nc.open_data("data/vertical_tester.nc")
        ds1.subset(variables = "e3t")
        ds.vertical_mean(ds1)
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y

        ds = nc.open_data("data/vertical_tester.nc")
        ds1 = nc.open_data("data/vertical_tester.nc")
        ds1.subset(variables = "e3t")
        ds1.run()
        ds.vertical_mean(ds1[0])
        ds.spatial_sum()
        y = ds.to_dataframe().one.sum()

        assert x == y

        version = nc.utils.cdo_version()
        if nc.utils.version_below(version, "1.9.8") == False:
            ds = nc.open_data("data/vertical_tester.nc")
            ds.vertical_integration("e3t")
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            assert ds2.to_dataframe().one.sum() == 0

            ds = nc.open_data(ff)
            ds.vertical_integration(depth_range=[2, 302], thickness="e3t")
            ds.spatial_max()
            assert ds.to_dataframe().one[0].astype("int") == 300


            ds = nc.open_data(ff)
            ds3 = nc.open_data(ff)
            ds3.subset(variable = "e3t")
            ds.vertical_integration(ds3)
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            ds2.to_dataframe().one.sum() == 0

            ds = nc.open_data(ff)
            ds3 = nc.open_data(ff)
            ds3.subset(variable = "e3t")
            ds3.run()
            ds.vertical_integration(ds3[0])
            ds.subset(variable = "one")
            ds.run()
            ds1 = nc.open_data(ff)
            ds1.assign(e3t = lambda x: x.e3t * (isnan(x.one) is False ) )
            ds1.subset(variables = "e3t")
            ds1.as_missing(0)
            ds1.vertical_sum()
            ds1.run()

            ds2 = ds.copy()
            ds2.subtract(ds1)
            ds2.spatial_sum()
            ds2.to_dataframe().one.sum() == 0



    def test_mean(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.885317325592041
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_max()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 10.37883186340332
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_min()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 4.02338171005249
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_sum()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 416.1104736328125
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_range()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.35545015335083
        n = len(nc.session_files())
        assert n == 1

    def test_int(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)
        tracker.subset(variables="t_an")
        tracker.vertical_interp(10)
        x = tracker.to_dataframe().t_an.values[0].astype("float")
        n = len(nc.session_files())
        assert n == 1

    def test_surface(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.subset(variables="t_an")
        tracker.top()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        assert x == 9.660191535949707
        n = len(nc.session_files())
        assert n == 1

    def test_bottom(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.subset(variables="t_an")
        tracker.bottom()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        assert x == 4.494192123413086
        n = len(nc.session_files())
        assert n == 1

    def test_bottom_error(self):
        n = len(nc.session_files())
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.subset(variables="t_an")
        new = tracker.copy()
        new.rename({"t_an": "test"})
        new.run()
        test = nc.open_data([tracker.current[0], new.current[0]])
        # with pytest.warns(UserWarning):
        with pytest.warns(UserWarning):
            test.bottom()
            test.run()
        n = len(nc.session_files())
        assert n == 4

    def test_bottom_mask(self):
        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.subset(variables="t_an")
        df1 = data.to_dataframe().reset_index()

        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.subset(variables="t_an")
        bottom = data.copy()
        bottom.bottom_mask()
        data.multiply(bottom)
        data.vertical_max()

        df2 = (
            data.to_dataframe()
            .reset_index()
            .loc[:, ["lon", "lat", "t_an"]]
            .dropna()
            .drop_duplicates()
        )
        df2 = df2.reset_index().drop(columns="index")
        x = (
            df1.loc[:, ["lon", "lat", "depth", "t_an"]]
            .dropna()
            .drop_duplicates()
            # .rename(columns = {"t_an":"t_an2"})
            .groupby(["lon", "lat"])
            .tail(1)
            .reset_index()
            .drop(columns=["index", "depth"])
            .sort_values(["lon", "lat"])
            .reset_index()
            .drop(columns="index")
            .equals(df2.sort_values(["lon", "lat"]).reset_index().drop(columns="index"))
        )
        assert x

    def test_bottom_mask_error(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))

        with pytest.raises(TypeError):
            data.bottom_mask()

        with pytest.raises(ValueError):
            data.vertical_interp()

        with pytest.raises(TypeError):
            data.vertical_interp(["x"])

    def test_bottom_mask_error2(self):
        data = nc.open_data(nc.create_ensemble("data/ensemble"))

        with pytest.raises(ValueError):
            data.merge("time")
            data.bottom_mask()

    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0
