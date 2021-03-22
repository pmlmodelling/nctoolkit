from nctoolkit.runthis import run_this
import subprocess

from nctoolkit.utils import is_curvilinear


def zonstat(self, stat="mean"):
    """Method to calculate the zonal statistic from a netCDF file"""

    for ff in self:
        if is_curvilinear(ff):
            raise TypeError(f"zonal_{stat} cannot be calculated for curvilinear grids.")

    cdo_command = f"cdo -zon{stat}"

    run_this(cdo_command, self, output="ensemble")


def zonal_mean(self):
    """
    Calculate the zonal mean for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the zonal mean for a dataset, do the following:

    >>> ds.zonal_mean()

    """
    zonstat(self, stat="mean")


def zonal_min(self):
    """
    Calculate the zonal minimum for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the zonal minimum for a dataset, do the following:

    >>> ds.zonal_min()
    """
    zonstat(self, stat="min")


def zonal_max(self):
    """
    Calculate the zonal maximum for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the zonal maximum for a dataset, do the following:

    >>> ds.zonal_max()
    """
    zonstat(self, stat="max")


def zonal_range(self):
    """
    Calculate the zonal range for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the zonal range for a dataset, do the following:

    >>> ds.zonal_range()

    """
    zonstat(self, stat="range")
