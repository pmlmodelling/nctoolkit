from nctoolkit.runthis import run_this
import subprocess

def is_curvilinear(ff):
    """Function to work out if a file contains a curvilinear grid"""
    cdo_result = subprocess.run(
        f"cdo sinfo {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return (
        len(
            [
                x
                for x in cdo_result.stdout.decode("utf-8").split("\n")
                if "curvilinear" in x
            ]
        )
        > 0
    )

def zonstat(self, stat="mean"):
    """Method to calculate the meridonial statistic from a netcdf file"""
    for ff in self:
        if is_curvilinear(ff):
            raise TypeError(f"meridonal_{stat} cannot be calculated for curvilinear grids.")
    cdo_command = f"cdo -mer{stat}"

    run_this(cdo_command, self, output="ensemble")


def meridonial_mean(self):
    """
    Calculate the meridonial mean for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    zonstat(self, stat="mean")


def meridonial_min(self):
    """
    Calculate the meridonial minimum for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    zonstat(self, stat="min")


def meridonial_max(self):
    """
    Calculate the meridonial maximum for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    zonstat(self, stat="max")


def meridonial_range(self):
    """
    Calculate the meridonial range for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    zonstat(self, stat="range")
