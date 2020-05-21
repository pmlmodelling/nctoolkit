
from nctoolkit.runthis import run_this


def ymonstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -ymon{stat}"

    run_this(cdo_command, self, output="ensemble")


def monthly_mean_climatology(self):
    """
    Calculate the monthly mean climatologies
    Defined as the minimum value in each month across all years. This applies to each file in an ensemble.
    """
    ymonstat(self, stat="mean")


def monthly_min_climatology(self):
    """
    Calculate the monthly minimum climatologies
    Defined as the minimum value in each month across all years. This applies to each file in an ensemble.
    """
    ymonstat(self, stat="min")


def monthly_max_climatology(self):
    """
    Calculate the monthly maximum climatologies
    Defined as the maximum value in each month across all years. This applies to each file in an ensemble.
    """
    ymonstat(self, stat="max")


def monthly_range_climatology(self):
    """
    Calculate the monthly range climatologies
    Defined as the range of value in each month across all years. This applies to each file in an ensemble.
    """
    ymonstat(self, stat="range")
