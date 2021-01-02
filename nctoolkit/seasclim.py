#jfrom nctoolkit.runthis import run_this
#j
#j
#jdef seasclim(self, stat="mean"):
#j    """Method to calculate the seasonal statistic from a function"""
#j    # create cdo call and run it
#j    cdo_command = f"cdo -yseas{stat}"
#j
#j    run_this(cdo_command, self, output="ensemble")
#j
#j
#jdef seasonal_mean_climatology(self):
#j    """
#j    Calculate a climatological seasonal mean
#j
#j    Parameters
#j    -------------
#j    window = int
#j        The size of the window for the calculation of the rolling sum
#j    """
#j
#j    seasclim(self, stat="mean")
#j
#j
#jdef seasonal_min_climatology(self):
#j    """
#j    Calculate a climatological seasonal min
#j    This is defined as the minimum value in each season across all years.
#j
#j    Parameters
#j    -------------
#j    window = int
#j        The size of the window for the calculation of the rolling sum
#j
#j    """
#j    seasclim(self, stat="min")
#j
#j
#jdef seasonal_max_climatology(self):
#j    """
#j    Calculate a climatological seasonal max
#j    This is defined as the maximum value in each season across all years.
#j
#j    Parameters
#j    -------------
#j    window = int
#j        The size of the window for the calculation of the rolling sum
#j
#j    """
#j    seasclim(self, stat="max")
#j
#j
#jdef seasonal_range_climatology(self):
#j    """
#j    Calculate a climatological seasonal range
#j    This is defined as the range of values in each season across all years.
#j
#j    Parameters
#j    -------------
#j    window = int
#j        The size of the window for the calculation of the rolling sum
#j
#j    """
#j    seasclim(self, stat="range")
