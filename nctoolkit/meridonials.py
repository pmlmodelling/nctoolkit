from nctoolkit.runthis import run_this
from nctoolkit.utils import is_curvilinear


def zonstat(self, stat="mean"):
    """Method to calculate the meridonial statistic from a netCDF file"""
    for ff in self:
        if is_curvilinear(ff):
            raise TypeError(
                f"meridonal_{stat} cannot be calculated for curvilinear grids."
            )
    cdo_command = f"cdo -mer{stat}"

    run_this(cdo_command, self, output="ensemble")


def meridonial_mean(self):
    """
    Calculate the meridonial mean for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the meridonial mean for a dataset, do the following:

    >>> ds.meridonial_mean()
    """
    zonstat(self, stat="mean")


def meridonial_min(self):
    """
    Calculate the meridonial minimum for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the meridonial minimum for a dataset, do the following:

    >>> ds.meridonial_min()
    """
    zonstat(self, stat="min")


def meridonial_max(self):
    """
    Calculate the meridonial maximum for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the meridonial maximum for a dataset, do the following:

    >>> ds.meridonial_max()

    """
    zonstat(self, stat="max")


def meridonial_range(self):
    """
    Calculate the meridonial range for each year/month combination in files.
    This applies to each file in an ensemble.

    Examples
    ------------
    If you want to calculate the meridonial range for a dataset, do the following:

    >>> ds.meridonial_max()
    """
    zonstat(self, stat="range")
