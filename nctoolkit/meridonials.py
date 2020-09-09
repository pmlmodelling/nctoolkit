from nctoolkit.runthis import run_this


def zonstat(self, stat="mean"):
    """Method to calculate the meridonial statistic from a netcdf file"""
    cdo_command = f"cdo -mer{stat}"

    run_this(cdo_command, self, output="ensemble")


def meridonial_mean(self):
    """
    Calculate the meridonial mean for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="mean")


def meridonial_min(self):
    """
    Calculate the meridonial minimum for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="min")


def meridonial_max(self):
    """
    Calculate the meridonial maximum for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="max")


def meridonial_range(self):
    """
    Calculate the meridonial range for each year/month combination in files. This applies to each file in an ensemble.
    """
    zonstat(self, stat="range")
