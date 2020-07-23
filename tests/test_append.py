import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import numpy as np
import os


ff = "data/sst.mon.mean.nc"

class TestAppend(unittest.TestCase):


    def test_append(self):
        new = nc.open_data(ff)
        new.mutate({"tos":"sst+273.15"})
        new.append(ff)

        assert len(new.current) == 2

        new = nc.open_data(ff)

        with self.assertRaises(ValueError) as context:
            new.append(ff)

        with self.assertRaises(ValueError) as context:
            new.append("xyz")

        new = nc.open_data(ff)
        with self.assertRaises(TypeError) as context:
            new.append()


        del new
        n = len(nc.session_files())
        self.assertEqual(n, 0)




if __name__ == '__main__':
    unittest.main()

