import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os
nc.options(lazy = True)


ff = "data/sst.mon.ltm.1981-2010.nc"


class TestApi2(unittest.TestCase):

    def test_url(self):
        tracker = nc.open_data(ff)
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst.values[0].astype("float")

        tracker = nc.open_data("ftp://ftp.cdc.noaa.gov/Datasets/COBE/sst.mon.ltm.1981-2010.nc")
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst.values[0].astype("float")

        print(x)
        print(y)
        assert x == y


    def test_corspace(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos":"sqrt(sst)"})
        tracker.cor_space("tos", "sst")
        x = tracker.to_dataframe().cor.values[0].astype("float")

        tracker1 = nc.open_data(ff)
        tracker1.select_variables("sst")
        tracker2 = nc.open_data(ff)

        tracker2.transmute({"tos":"sqrt(sst)"})
        tracker2.run()

        print("working")
        tracker3 = nc.cor_space(tracker1, tracker2)
        print("working1")

        y = tracker3.to_dataframe().cor.values[0].astype("float")
        print(x)
        print(y)
        assert x == y


        tracker = nc.open_data(ff)
        with self.assertRaises(ValueError) as context:
            tracker3 = nc.cor_space(tracker, tracker2)

        with self.assertRaises(ValueError) as context:
            tracker3 = nc.cor_time(tracker, tracker2)



        with self.assertRaises(TypeError) as context:
            tracker3 = nc.cor_space("x", tracker2)

        with self.assertRaises(TypeError) as context:
            tracker3 = nc.cor_space(tracker, "x")

if __name__ == '__main__':
    unittest.main()

