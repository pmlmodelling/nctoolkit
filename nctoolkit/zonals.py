
from nctoolkit.runthis import run_this


def zonstat(self, stat="mean"):
    """Method to calculate the zonal statistic from a netcdf file"""
    cdo_command = f"cdo -zon{stat}"

    run_this(cdo_command, self, output="ensemble")


def zonal_mean(self):
    """
    Calculate the zonal mean for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="mean")


def zonal_min(self):
    """
    Calculate the zonal minimum for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="min")


def zonal_max(self):
    """
    Calculate the zonal maximum for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="max")


def zonal_range(self):
    """
    Calculate the zonal range for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="range")



