import unittest
import nchack as nc
nc.options(lazy= False)
nc.options(thread_safe = True)
import pandas as pd
import xarray as xr
import os


ff = "data/sst.mon.mean.nc"

class TestShow(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_times(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep(range(0,12))
        tracker.release()
        x = len(tracker.times())

        self.assertEqual(x, 12)

    def test_times2(self):
        tracker = nc.open_data(ff)
        x = tracker.times()
        tracker.split("year")
        y = tracker.times()
        self.assertEqual(x,y)


    def test_months(self):
        tracker = nc.open_data(ff)
        tracker.select_months([1,2])
        tracker.release()
        x = tracker.months()

        self.assertEqual(x, [1,2])

    def test_months1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990, 1991])
        tracker.select_months([1,2])
        tracker.split("year")
        tracker.release()
        x = tracker.months()

        self.assertEqual(x, [1,2])


    def test_years(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990,1999])
        tracker.release()
        x = tracker.years()

        self.assertEqual(x, [1990,1999])

    def test_years1(self):
        tracker = nc.open_data(ff)
        tracker.select_years([1990,1999])
        tracker.split("year")
        x = tracker.years()

        self.assertEqual(x, [1990,1999])

    def test_nc_years(self):
        x = nc.nc_years(ff)

        self.assertEqual(len(x), len(range(1850, 2019)))

    def test_nc_variables(self):
        x = nc.nc_variables(ff)

        self.assertEqual(x, ["sst"])

    def test_levels(self):
        tracker = nc.open_data("data/woa18_decav_t01_01.nc")
        x = tracker.levels()
        self.assertEqual([x[0], x[4]], [0.0,20.0])

    def test_levels2(self):
        tracker = nc.open_data(["data/woa18_decav_t01_01.nc","data/woa18_decav_t02_01.nc"])
        x = tracker.levels()
        self.assertEqual([x[0], x[4]], [0.0,20.0])


    def test_attributes2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1])
        tracker.split("yearmonth")
        x = tracker.attributes()
        y = 'sst:\n  long_name = "Monthly Means of Global Sea Surface Temperature"\n  units = "degC"\n  missing_value = "1.000000e+20"\n  var_desc = "Sea Surface Temperature"\n  dataset = "COBE-SST2 Sea Surface Temperature"\n  statistic = "Mean"\n  parent_stat = "Individual obs"\n  level_desc = "Surface"\n  actual_range = -2.043\nGlobal:\n  title = "created 12/2013 from data provided by JRA"\n  platform = "Analyses"\n  citation = "Hirahara, S., Ishii, M., and Y. Fukuda,2014: Centennial-scale sea surface temperature analysis and its uncertainty. J of Climate, 27, 57-75. http://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00837.1"\n  Conventions = "CF-1.2"\n  References = "http://www.esrl.noaa.gov/psd/data/gridded/cobe2.html"\n  dataset_title = "COBE-SST2 Sea Surface Temperature and Ice"\n  original_source = "https://climate.mri-jma.go.jp/pub/ocean/cobe-sst2/"\n'

        self.assertEqual(len(x), len(y))


    def test_attributes(self):
        tracker = nc.open_data(ff)
        x = tracker.attributes()
        y = 'sst:\n  long_name = "Monthly Means of Global Sea Surface Temperature"\n  units = "degC"\n  missing_value = "1.000000e+20"\n  var_desc = "Sea Surface Temperature"\n  dataset = "COBE-SST2 Sea Surface Temperature"\n  statistic = "Mean"\n  parent_stat = "Individual obs"\n  level_desc = "Surface"\n  actual_range = -2.043\nGlobal:\n  title = "created 12/2013 from data provided by JRA"\n  platform = "Analyses"\n  citation = "Hirahara, S., Ishii, M., and Y. Fukuda,2014: Centennial-scale sea surface temperature analysis and its uncertainty. J of Climate, 27, 57-75. http://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00837.1"\n  Conventions = "CF-1.2"\n  References = "http://www.esrl.noaa.gov/psd/data/gridded/cobe2.html"\n  dataset_title = "COBE-SST2 Sea Surface Temperature and Ice"\n  original_source = "https://climate.mri-jma.go.jp/pub/ocean/cobe-sst2/"\n'

        self.assertEqual(x,y)

    def test_global_attributes2(self):
        tracker = nc.open_data(ff)
        tracker.select_timestep([0,1])
        tracker.split("yearmonth")
        x = tracker.global_attributes()
        y = 'Global:\n  title = "created 12/2013 from data provided by JRA"\n  platform = "Analyses"\n  citation = "Hirahara, S., Ishii, M., and Y. Fukuda,2014: Centennial-scale sea surface temperature analysis and its uncertainty. J of Climate, 27, 57-75. http://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00837.1"\n  Conventions = "CF-1.2"\n  References = "http://www.esrl.noaa.gov/psd/data/gridded/cobe2.html"\n  dataset_title = "COBE-SST2 Sea Surface Temperature and Ice"\n  original_source = "https://climate.mri-jma.go.jp/pub/ocean/cobe-sst2/"\n'


    def test_global_attributes(self):
        tracker = nc.open_data(ff)
        x = tracker.global_attributes()
        y = 'Global:\n  title = "created 12/2013 from data provided by JRA"\n  platform = "Analyses"\n  citation = "Hirahara, S., Ishii, M., and Y. Fukuda,2014: Centennial-scale sea surface temperature analysis and its uncertainty. J of Climate, 27, 57-75. http://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00837.1"\n  Conventions = "CF-1.2"\n  References = "http://www.esrl.noaa.gov/psd/data/gridded/cobe2.html"\n  dataset_title = "COBE-SST2 Sea Surface Temperature and Ice"\n  original_source = "https://climate.mri-jma.go.jp/pub/ocean/cobe-sst2/"\n'

        self.assertEqual(x,y)

if __name__ == '__main__':
    unittest.main()

