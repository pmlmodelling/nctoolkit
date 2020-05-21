
from nctoolkit.runthis import run_this


def seasstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -seas{stat}"

    run_this(cdo_command, self, output="ensemble")


def seasonal_mean(self):
    """
    Calculate the seasonal mean for each year. Applies at the grid cell level.
    """
    seasstat(self, stat="mean")


def seasonal_min(self):
    """
    Calculate the seasonal minimum for each year. Applies at the grid cell level.
    """
    seasstat(self, stat="min")


def seasonal_max(self):
    """
    Calculate the seasonal maximum for each year. Applies at the grid cell level.
    """
    seasstat(self, stat="max")


def seasonal_range(self):
    """
    Calculate the seasonal range for each year. Applies at the grid cell level.
    """
    seasstat(self, stat="range")
