import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"



class TestCrop:
    def test_matchpoint(self):

        print("test 1")
        depths = nc.open_data("data/matchpoint_depths.nc", checks=False)

        ensemble = nc.create_ensemble("data/matchpoint")[0:3]

        ds = nc.open_data("data/matchpoint/amm7_1d_20000301_20000331_ptrc_T.nc", checks=False)
        levels = ds.levels
        levels += levels
        ds.subset(time = [0])
        depths = nc.open_data("data/matchpoint_depths.nc", checks=False)
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()

        ds = nc.open_data("data/matchpoint/amm7_1d_20000301_20000331_ptrc_T.nc", checks=False)
        ds.subset(time = [0])
        ds.run()

        matcher = nc.open_matchpoint()
        # depths = ds.levels
        # df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)
        matcher.matchup()


        matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias
        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)



        print("test 2")
        matcher = nc.open_matchpoint()
        depths = ds.levels
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)
        with pytest.raises(ValueError):
            matcher.add_data(ds, variables = "N3_n")



        matcher = nc.open_matchpoint()
        depths = ds.levels
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)

        depths = nc.open_data("data/matchpoint_depths.nc", checks=False)

        ensemble = nc.create_ensemble("data/matchpoint")[0:3]

        ds = nc.open_data("data/matchpoint/amm7_1d_20000301_20000331_ptrc_T.nc", checks=False)
        levels = ds.levels
        levels += levels
        ds.subset(time = [0])
        depths = nc.open_data("data/matchpoint_depths.nc", checks=False)
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()
        df = df.sort_values(by = ["lon", "lat", "depth"]).reset_index(drop=True)    
        ds = nc.open_data("data/matchpoint/amm7_1d_20000301_20000331_ptrc_T.nc", checks=False)
        ds.subset(time = [0])
        ds.run()
        matcher = nc.open_matchpoint()
        depths = ds.levels
        matcher.add_data(ds, variables = "N3_n", depths = depths)

        with pytest.raises(ValueError):
            matcher.add_data(ds, variables = "N3_n")
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.matchup()


        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)



        #print("test 3")

        print("test 4")
        ds = nc.open_data("data/emodnet_test.nc", checks=False)
        ds.regrid(pd.DataFrame({"lon": [0.15, 0.175], "lat" : [54.1, 54.12]}) )
        df = ds.to_dataframe().reset_index()
        ds = nc.open_data("data/emodnet_test.nc", checks=False)
        matcher = nc.open_matchpoint()
        matcher.add_data(ds)
        matcher.add_points(df.loc[:,["lon", "lat"]])
        matcher.matchup()
        assert matcher.values.rename(columns = {"elevation":"values_123"}).merge(df).assign(bias = lambda x: np.abs(x.values_123 - x.elevation)).bias.max() < 0.00001

        assert len(matcher.values) == len(df)

        print("test 7")
        ds = nc.open_data("data/sst.mon.mean.nc", checks=  False) 
        df = pd.DataFrame({"lon":[-20], "lat":56})

        matcher = nc.open_matchpoint()
        matcher.add_data(ds)
        matcher.add_points(df.loc[:,["lon", "lat"]])
        matcher.matchup()
        matcher.values
        ds.regrid(df)
        df_test = ds.to_dataframe().reset_index().drop_duplicates()
        df_test["month"] = [x.month for x in df_test.time]
        df_test["day"] = [x.day for x in df_test.time]
        df_test["year"] = [x.year for x in df_test.time]
        assert df_test.rename(columns = {"sst":"test"}).merge(matcher.values).assign(bias = lambda x: np.abs(x.sst - x.test)).bias.max() <  0.00001
        assert len(matcher.values) == 360




        ds = nc.open_data("data/woa18_decav_t01_01.nc", checks=False)
        df = pd.DataFrame({"lon":np.repeat(-20, 8), "lat":np.repeat(55, 8), "depth":np.arange(-7, 1)})
        df_matched = ds.match_points(df, max_extrap=6)
        assert np.isnan(df_matched.query("depth == -7").t_an[0])
        assert df_matched.query("depth == -5").t_an.values[0] == df_matched.query("depth == 0").t_an.values[0]
#
#
