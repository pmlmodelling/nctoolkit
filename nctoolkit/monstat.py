
from nctoolkit.runthis import run_this


def monstat(self, stat="mean"):
    """Method to calculate the monthly statistic from a netcdf file"""
    cdo_command = f"cdo -mon{stat}"

    run_this(cdo_command, self, output="ensemble")


def monthly_mean(self):
    """
    Calculate the monthly mean for each year/month combination in files. This applies to each file in an ensemble.
    """
    monstat(self, stat="mean")


def monthly_min(self):
    """
    Calculate the monthly minimum for each year/month combination in files. This applies to each file in an ensemble.
    """
    monstat(self, stat="min")


def monthly_max(self):
    """
    Calculate the monthly maximum for each year/month combination in files. This applies to each file in an ensemble.
    """
    monstat(self, stat="max")


def monthly_range(self):
    """
    Calculate the monthly range for each year/month combination in files. This applies to each file in an ensemble.
    """
    monstat(self, stat="range")
