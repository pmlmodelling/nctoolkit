
from nctoolkit.runthis import run_this


def yearlystat(self, stat="mean"):
    """Function to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -year{stat}"

    run_this(cdo_command, self, output="ensemble")


def annual_mean(self):
    """
    Calculate the annual mean for each variable
    """
    yearlystat(self, stat="mean")


def annual_min(self):
    """
    Calculate the annual minimum for each variable
    """
    yearlystat(self, stat="min")


def annual_max(self):
    """
    Calculate the annual maximum for each variable
    """
    yearlystat(self, stat="max")


def annual_range(self):
    """
    Calculate the annual range for each variable
    """
    yearlystat(self, stat="range")
