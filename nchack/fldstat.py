from .session import nc_safe
import copy
from .runthis import run_this
from .temp_file import temp_file
from .runthis import run_cdo
from .runthis import tidy_command
from .cleanup import cleanup
from .cleanup import disk_clean

import subprocess

def cdo_version():
    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


def fldstat(
    self, stat="mean",
):
    """Method to calculate the spatial stat from a netcdf"""
    if cdo_version() in ["1.9.3"]:
        self.run()

    cdo_command = f"cdo -fld{stat}"

    run_this(cdo_command, self, output="ensemble")
    if cdo_version() in ["1.9.3"]:
        self.run()


def spatial_mean(self):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.
    """

    return fldstat(self, stat="mean")


def spatial_min(self):
    """
    Calculate a spatial minimum of variables. This is performed for each time step.

    """
    return fldstat(self, stat="min")


def spatial_max(self):
    """
    Calculate a spatial maximum of variables. This is performed for each time step.
    """

    return fldstat(self, stat="max")


def spatial_range(self):
    """
    Calculate a spatial range of variables. This is performed for each time step.
    """

    return fldstat(self, stat="range")


def spatial_sum(self, by_area=False):
    """
    Calculate the spatial sum of variables. This is performed for each time step.

    Parameters
    --------------
    by_area : boolean
        Set to True if you want to multiply the values by the grid cell area before summing over space. Default is False.
    """

    if isinstance(by_area, bool) == False:
        raise TypeError("by_area is not boolean")

    if (type(self.current)) is str or (by_area == False):

        if by_area:
            self.run()

            cdo_command = f"cdo -fldsum -mul {self.current} -gridarea "
        else:
            cdo_command = "cdo -fldsum"

        run_this(cdo_command, self, output="ensemble")

        return None

    new_files = []
    new_commands = []
    for ff in self:

        target = temp_file("nc")
        cdo_command = f"cdo -fldsum -mul {ff} -gridarea {ff} {target}"
        cdo_command = tidy_command(cdo_command)
        target = run_cdo(cdo_command, target=target)
        new_files.append(target)
        new_commands.append(cdo_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()
    self.disk_clean()


def spatial_percentile(self, p=None):
    """
    Calculate the spatial sum of variables. This is performed for each time step.
    Parameters
    -------------
    p: int or float
        Percentile to calculate. 0<=p<=100.
    """

    if p is None:
        raise ValueError("Please supply a percentile")

    if type(p) not in (int, float):
        raise ValueError(f"{str(p)} is not a valid percentile")
    if (p < 0) or (p > 100):
        raise ValueError(f"p: {str(p)} is not between 0 and 100!")

    cdo_command = f"cdo -fldpctl,{str(p)}"

    run_this(cdo_command, self, output="ensemble")
