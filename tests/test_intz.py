import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest
import warnings


class TestVerts:



    def test_zleve(self):
        ds = nc.open_data("data/foo.nc", checks=False)
        depths = ds.copy()
        depths.subset(variables = "e3t")
        thickness = ds.copy()
        thickness.subset(variables = "e3t")
        thickness / 2
        depths.vertical_cumsum()
        depths.rename({"e3t":"depth"})
        depths - thickness
        ds.append(depths)
        ds.merge()
        df = ds.to_dataframe().reset_index().loc[:,["nav_lon", "nav_lat", "depth", "N1_p"]].dropna().query("depth > 10").reset_index(drop = True).sample(100).sort_values("depth").reset_index(drop = True)
        ds.drop(variables = "depth")
        ds.vertical_interp(levels = list(df.depth), thickness = "e3t")
        df_comp = (
        ds
            .to_dataframe()
            .dropna()
            .reset_index()
            .loc[:,["depth", "nav_lon", "nav_lat", "N1_p"]]
            .dropna()
            .drop_duplicates()
            .rename(columns = {"N1_p":"N_int"})
            .merge(df)
            
           )
        assert len(df_comp.query("N_int != N1_p")) == 0

        del thickness
        del depths
        del ds

