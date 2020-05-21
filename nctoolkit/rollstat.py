
from nctoolkit.runthis import run_this


def rollstat(self, window=None, stat="mean"):
    """Method to calculate the monthly statistic from a netcdf file"""
    # check window supplied is valid

    if window is None:
        raise ValueError("No window was supplied")

    if type(window) is not int:
        raise TypeError("The window supplied is not numeric!")

    if window < 1:
        raise ValueError(f"{window} is not a valid window!")

    # create the cdo call and run it
    cdo_command = f"cdo -run{stat},{str(window)}"
    run_this(cdo_command, self, output="ensemble")


def rolling_mean(self, window=None):
    """
    Calculate a rolling mean based on a window

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling mean
    """
    rollstat(self, window=window, stat="mean")


def rolling_min(self, window=None):
    """
    Calculate a rolling minimum based on a window

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling minimum
    """
    rollstat(self, window=window, stat="min")


def rolling_max(self, window=None):
    """
    Calculate a rolling maximum based on a window

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling maximum
    """
    rollstat(self, window=window, stat="max")


def rolling_range(self, window=None):
    """
    Calculate a rolling range based on a window

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling range
    """
    rollstat(self, window=window, stat="range")


def rolling_sum(self, window=None):
    """
    Calculate a rolling sum based on a window

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    """
    rollstat(self, window=window, stat="sum")
