import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestTemporals:
    def test_temporals_align(self):
        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.tmean(align = "left")
        ds.run()
        assert [x.year for x in ds.times][0] == 1970
        
        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.tmean(align = "right")
        ds.run()
        assert [x.year for x in ds.times][0] == 1999
        
        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.tmean("year", align = "right")
        ds.run()
        assert [x.month for x in ds.times][0] == 12


    def test_temporals_mean(self):
        version = nc.utils.cdo_version()
        n = len(nc.session_files())
        assert n == 0

        if nc.utils.version_below(version, "1.9.8") == False:
            ds = nc.open_data(ff)
            ds.na_count()
            ds.spatial_sum()
            ds.to_dataframe()
            assert ds.to_dataframe().sst.values[0] == 295200.0

            ds = nc.open_data(ff)
            ds.na_frac()
            ds.spatial_sum()
            ds.to_dataframe()
            assert ds.to_dataframe().sst.values[0] == 820.0 

            del ds

        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["month"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        ds = nc.open_data("data/sst.mon.mean.nc")
        ds.tvar()
        ds.spatial_sum()
        ds.to_dataframe()
        assert ds.to_dataframe().sst.values[0] == 19726.29296875 

        del ds

        assert x == 12.751260757446289 

        tracker = nc.open_data(ff)
        tracker.tmean(["month", "day"])
        tracker.spatial_mean()
        y = float(tracker.to_dataframe().sst.values[0])
        assert y == x 

        tracker = nc.open_data(ff)
        tracker.tpercentile(over = ["month"], p =0.05)
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        tracker = nc.open_data(ff)
        tracker.tpercentile( over = ["month", "day"], p = 0.05)
        tracker.spatial_mean()
        y = float(tracker.to_dataframe().sst.values[0])
        assert y == x 

        tracker = nc.open_data()
        with pytest.raises(ValueError):
            tracker.tmean()

        with pytest.raises(ValueError):
            tracker.tpercentile(p = 0.05)

        # annual mean

        tracker = nc.open_data(ff)
        tracker.tmean(["year"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x ==  15.243741989135742  




        # daily mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["day"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x == 12.751260757446289 




        # seasonal mean climatology

        tracker = nc.open_data(ff)
        tracker.tmean(["season"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])

        assert x == 12.944276809692383 


        # annual seasonal mean

        tracker = nc.open_data(ff)
        tracker.tmean(["season", "year"])
        tracker.spatial_mean()
        x = float(tracker.to_dataframe().sst.values[0])


        assert x == 12.24020767211914 

        # daily mean

        tracker = nc.open_data(ff)
        tracker.tmean(["day", "month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 12.573156356811523 



        # monthly mean

        tracker = nc.open_data(ff)
        tracker.tmean(["month", "year"])
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 12.573156356811523 









    def test_temporals_max(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["month"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 24.663002014160156 


        # annual max

        tracker = nc.open_data(ff)
        tracker.tmax(["year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 28.94500160217285  


        # daily max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["day"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 24.663002014160156 




        # seasonal max climatology

        tracker = nc.open_data(ff)
        tracker.tmax(["season"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 25.29400062561035 




        # daily max

        tracker = nc.open_data(ff)
        tracker.tmax(["day", "month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 23.31300163269043 



        # monthly max

        tracker = nc.open_data(ff)
        tracker.tmax(["month", "year"])
        tracker.spatial_max()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 23.31300163269043 









    def test_temporals_min(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["month"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8410000801086426 


        # annual min

        tracker = nc.open_data(ff)
        tracker.tmin(["year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.852000117301941 




        # daily min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["day"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8410000801086426 


        # seasonal min climatology

        tracker = nc.open_data(ff)
        tracker.tmin(["season"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.8560000658035278 




        # daily min

        tracker = nc.open_data(ff)
        tracker.tmin(["day", "month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == -1.6100001335144043  



        # monthly min

        tracker = nc.open_data(ff)
        tracker.tmin(["month", "year"])
        tracker.spatial_min()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) ==  -1.6100001335144043 



    def test_temporals_range(self):
        n = len(nc.session_files())
        assert n == 0


        # monthly climatology

        tracker = nc.open_data(ff)
        tracker.trange(["month"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 3.8899998664855957 


        # annual range

        tracker = nc.open_data(ff)
        tracker.trange(["year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 20.002002716064453 


        # daily range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["day"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 3.8899998664855957 




        # seasonal range climatology

        tracker = nc.open_data(ff)
        tracker.trange(["season"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 6.654000759124756 




        # daily range

        tracker = nc.open_data(ff)
        tracker.trange(["day", "month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]


        assert float(x) == 0



        # monthly range

        tracker = nc.open_data(ff)
        tracker.trange(["month", "year"])
        tracker.spatial_range()
        x = tracker.to_dataframe().sst.values[0]

        assert float(x) == 0


