
from .runthis import run_this

def seasstat(self, stat = "mean"):
    """Method to calculate the seasonal statistic from a function"""
    # create cdo call and run it
    cdo_command = f"cdo -yseas{stat}"

    run_this(cdo_command, self,  output = "ensemble")


def seasonal_mean_climatology(self):

    """
    Calculate a seasonal mean climatology

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    """

    return seasstat(self, stat = "mean")

def seasonal_min_climatology(self):
    """
    Calculate a seasonal minimum climatology

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    return seasstat(self, stat = "min")

def seasonal_max_climatology(self):
    """
    Calculate a seasonal maximum climatology

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    return seasstat(self, stat = "max")

def seasonal_range_climatology(self):
    """
    Calculate a seasonal range climatology

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    return seasstat(self, stat = "range")
