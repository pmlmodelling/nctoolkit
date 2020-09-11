import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import warnings


class TestVerts:
    def test_mean(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.885317325592041
        n = len(nc.session_files())
        assert n == 1

    def test_max(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_max()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 10.37883186340332
        n = len(nc.session_files())
        assert n == 1

    def test_min(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_min()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 4.02338171005249
        n = len(nc.session_files())
        assert n == 1

    def test_sum(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_sum()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 416.1104736328125
        n = len(nc.session_files())
        assert n == 1

    def test_range(self):
        ff = "data/woa18_decav_t01_01.nc"

        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_range()
        tracker.spatial_mean()
        x = tracker.to_xarray().t_an.values[0][0][0].astype("float")
        assert x == 6.35545015335083
        n = len(nc.session_files())
        assert n == 1

    def test_int(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)
        tracker.select_variables("t_an")
        tracker.vertical_interp(10)
        x = tracker.to_dataframe().t_an.values[0].astype("float")
        n = len(nc.session_files())
        assert n == 1

    def test_surface(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
        tracker.surface()
        tracker.spatial_mean()
        x = tracker.to_dataframe().t_an.values[0].astype("float")

        assert x == 9.660191535949707
        n = len(nc.session_files())
        assert n == 1

    def test_bottom(self):
        ff = "data/woa18_decav_t01_01.nc"
        tracker = nc.open_data(ff)

        tracker.select_variables("t_an")
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

        tracker.select_variables("t_an")
        new = tracker.copy()
        new.rename({"t_an": "test"})
        new.run()
        test = nc.open_data([tracker.current, new.current])
        # with pytest.warns(UserWarning):
        with pytest.warns(UserWarning):
            test.bottom()
            test.run()
        n = len(nc.session_files())
        assert n == 4

    def test_bottom_mask(self):
        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.select_variables("t_an")
        df1 = data.to_dataframe().reset_index()

        data = nc.open_data("data/woa18_decav_t01_01.nc")
        data.select_variables("t_an")
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
            data.merge_time()
            data.bottom_mask()

    def test_empty(self):
        n = len(nc.session_files())
        assert n == 0
