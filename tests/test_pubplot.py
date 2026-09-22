import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest
import re


ff = "data/sst.mon.mean.nc"

class TestCrop:
    def test_pub_plot(self):

        # generate a random file name
        out_file = "asdfkjbuwnjlajksdfi.png"

        ds = nc.open_data("data/sst.mon.mean.nc", checks = False)

        with pytest.raises(ValueError):
            ds.pub_plot()


        ds.subset(time = 0)
        ds.pub_plot(out = out_file, land = "grey")

        with pytest.raises(ValueError, match=r"Did you mean"):
            ds.pub_plot(grid_colourrs = "none")

        with pytest.raises(ValueError, match=r"not a valid"):
            ds.pub_plot(invalid = None)

        assert os.path.exists(out_file)
        # get file size
        # this needs to be improved so it figures if the file is similar to the one in the repo
        assert os.path.getsize(out_file) > 140000 and os.path.getsize(out_file) < 150000

        with pytest.raises(ValueError):
            ds.pub_plot(mid_point = -1000)
        with pytest.raises(ValueError):
            ds.pub_plot(mid_point = 1000)


        ds.assign(tos = lambda x: x.sst + 273.15)
        ds.pub_plot(var = "sst", out = out_file, land = "grey")

        assert os.path.exists(out_file)
        # get file size
        # this needs to be improved so it figures if the file is similar to the one in the repo
        assert os.path.getsize(out_file) > 140000 and os.path.getsize(out_file) < 150000

        # value error check

        with pytest.raises(ValueError):
            ds.pub_plot(legend_position = "blah")

        with pytest.raises(ValueError):
            ds.pub_plot(scale = "blah")

        with pytest.raises(ValueError):
            ds.pub_plot(coast = "blah")

        with pytest.raises(TypeError):
            ds.pub_plot(land = 1)

        ds1 = ds.copy()
        ds1.assign(tos = lambda x: x.sst + 273.15)

        with pytest.raises(ValueError):
            ds1.pub_plot()
        with pytest.raises(ValueError):
            ds1 = nc.open_data("data/sst.mon.mean.nc", checks = False)
            ds1.pub_plot()
        
        with pytest.raises(ValueError):
            ds1.pub_plot()


        from difflib import SequenceMatcher

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()
        
        with pytest.raises(ValueError):
            ds.pub_plot(all_wrong = False)

        with pytest.raises(ValueError):
            ds.pub_plot(lands = "grey")

        os.remove(out_file)

    def test_pub_plot_options(self):
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        import cartopy.crs as ccrs

        out_file = "pubplot_options_test.png"

        ds = nc.open_data(ff, checks = False)
        ds.subset(time = 0)

        ds.pub_plot(out = out_file, dpi = 50)
        # auto size is 5 inches tall
        assert mpimg.imread(out_file).shape[0] == 5 * 50
        os.remove(out_file)
        plt.close("all")

        ds.pub_plot(coast = None)
        plt.close("all")

        ds_global = nc.open_data("data/sst.mon.ltm.1981-2010.nc", checks = False)
        ds_global.subset(time = 0, variables = "sst")

        ds_global.pub_plot()
        assert isinstance(plt.gcf().axes[0].projection, ccrs.Robinson)
        plt.close("all")

        ds_global.pub_plot(projection = ccrs.PlateCarree())
        assert isinstance(plt.gcf().axes[0].projection, ccrs.PlateCarree)
        plt.close("all")

        ds.pub_plot(legend = "Temp", legend_position = "bottom")
        assert plt.gcf().axes[1].get_xlabel() == "Temp"
        plt.close("all")

        from cartopy.mpl.gridliner import Gridliner

        def n_grid_labels():
            fig = plt.gcf()
            fig.canvas.draw()
            gls = [a for a in fig.axes[0].artists if isinstance(a, Gridliner)]
            return sum(a.get_visible() for gl in gls for a in gl.label_artists)

        ds.pub_plot()
        assert n_grid_labels() > 0
        plt.close("all")

        ds.pub_plot(grid_labels = False)
        assert n_grid_labels() == 0
        plt.close("all")

        # global Robinson maps also label the curved edges
        ds_global.pub_plot(grid_labels = False)
        assert n_grid_labels() == 0
        plt.close("all")

        with pytest.raises(TypeError):
            ds.pub_plot(grid_labels = "no")
