import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestFinal(unittest.TestCase):

    def test_cleanall(self):
        safe = nc.session.nc_safe
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.run()
        safe = nc.session.nc_safe
        nc.clean_all()
        x = len([ff for ff in safe if os.path.exists(ff)])

        self.assertEqual(x, 0)



if __name__ == '__main__':
    unittest.main()

