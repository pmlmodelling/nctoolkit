
from .session import nc_safe
import copy
from .runthis import run_this
from .temp_file import temp_file
from .runthis import run_cdo
from .cleanup import cleanup


def fldstat(self, stat = "mean",):
    """Method to calculate the spatial stat from a netcdf"""

    cdo_command = "cdo -fld" + stat

    run_this(cdo_command, self,  output = "ensemble")

def spatial_mean(self):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.
    """

    return fldstat(self, stat = "mean")

def spatial_min(self):
    """
    Calculate a spatial minimum of variables. This is performed for each time step.

    """
    return fldstat(self, stat = "min")

def spatial_max(self):
    """
    Calculate a spatial maximum of variables. This is performed for each time step.
    """

    return fldstat(self, stat = "max")

def spatial_range(self):
    """
    Calculate a spatial range of variables. This is performed for each time step.
    """

    return fldstat(self, stat = "range")

def spatial_sum(self, by_area = False):
    """
    Calculate the spatial sum of variables. This is performed for each time step.

    Parameters
    --------------
    by_area : boolean
        Set to True if you want to multiply the values by the grid cell area before summing over space. Default is False.
    """

    if type(self.current) is str or by_area == False:

        if by_area:
            self.release()

            cdo_command = "cdo -fldsum -mul " + self.current  + " -gridarea "
        else:
            cdo_command = "cdo -fldsum"

        run_this(cdo_command, self,  output = "ensemble")

        return None


    new_files = []
    new_commands = []
    for ff in self.current:

        target = temp_file("nc")
        cdo_command = "cdo -fldsum -mul " + ff  + " -gridarea " + ff + " " +  target
        target = run_cdo(cdo_command, target = target)
        new_files.append(target)
        new_commands.append(cdo_command)


    self.history+=new_commands
    self._hold_history = copy.deepcopy(self.history)

    for ff in self.current:
        if ff in nc_safe:
            nc_safe.remove(ff)

    self.current = new_files

    for ff in self.current:
        nc_safe.append(ff)


    cleanup()





def spatial_percentile(self, p = 50):
    """
    Calculate the spatial sum of variables. This is performed for each time step.
    Parameters
    -------------
    p: int or float
        Percentile to calculate. 0<=p<=100.
    """

    if type(p) not in (int, float):
        raise ValueError(str(p) + " is not a valid percentile")
    if p < 0 or p > 100:
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    cdo_command = "cdo -fldpctl," + str(p)

    run_this(cdo_command, self,  output = "ensemble")




