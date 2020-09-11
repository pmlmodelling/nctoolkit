import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.ltm.1981-2010.nc"


class TestApi2:
    def test_corspace(self):
        tracker = nc.open_data(ff)
        tracker.mutate({"tos": "sqrt(sst)"})
        tracker.cor_space("tos", "sst")
        x = tracker.to_dataframe().cor.values[0].astype("float")

        tracker1 = nc.open_data(ff)
        tracker1.select_variables("sst")
        tracker2 = nc.open_data(ff)

        tracker2.transmute({"tos": "sqrt(sst)"})
        tracker2.run()

        tracker3 = nc.cor_space(tracker1, tracker2)

        y = tracker3.to_dataframe().cor.values[0].astype("float")
        assert x == y

        tracker = nc.open_data(ff)
        with pytest.raises(ValueError):
            tracker3 = nc.cor_space(tracker, tracker2)

        with pytest.raises(ValueError):
            tracker3 = nc.cor_time(tracker, tracker2)

        with pytest.raises(TypeError):
            tracker3 = nc.cor_space("x", tracker2)

        with pytest.raises(TypeError):
            tracker3 = nc.cor_space(tracker, "x")
