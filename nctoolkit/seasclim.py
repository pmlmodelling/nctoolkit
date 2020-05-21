
from nctoolkit.runthis import run_this


def seasstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""
    # create cdo call and run it
    cdo_command = f"cdo -yseas{stat}"

    run_this(cdo_command, self, output="ensemble")


def seasonal_mean_climatology(self):
    """
    Calculate a climatological seasonal mean

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    """

    seasstat(self, stat="mean")


def seasonal_min_climatology(self):
    """
    Calculate a climatological seasonal min
    This is defined as the minimum value in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    seasstat(self, stat="min")


def seasonal_max_climatology(self):
    """
    Calculate a climatological seasonal max
    This is defined as the maximum value in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    seasstat(self, stat="max")


def seasonal_range_climatology(self):
    """
    Calculate a climatological seasonal range
    This is defined as the range of values in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    seasstat(self, stat="range")
