import unittest
import nctoolkit as nc
nc.options(lazy= True)
import pandas as pd
import xarray as xr
import os


class TestCreate(unittest.TestCase):

    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_create(self):
        ensemble = nc.create_ensemble("data/ensemble")
        assert len(ensemble) == 60

        with self.assertRaises(ValueError) as context:
            ensemble = nc.create_ensemble("akdi2nkciihj2jkjjj")

        with self.assertRaises(ValueError) as context:
            ensemble = nc.create_ensemble(".", recursive = False)

if __name__ == '__main__':
    unittest.main()

