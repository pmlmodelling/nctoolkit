import copy

from .temp_file import temp_file
from .session import nc_safe
from .runthis import run_cdo
from .cleanup import cleanup
from .cleanup import disk_clean
from .show import nc_variables


def cor(self, var1 = None, var2 = None, method = "fld"):

    if var1 is None or var2 is None:
        raise ValueError("Both variables are not given")

    # this cannot be chained. So release
    self.release()

    new_files = []
    new_commands = []

    for ff in self:
        if var1 not in nc_variables(ff):
            raise ValueError(var1 + " is not in the dataset")

        if var2 not in nc_variables(ff):
            raise ValueError(var2 + " is not in the dataset")

        # create the temp file for targeting
        target = temp_file(".nc")

        # create the cdo command and run it
        cdo_command = "cdo -L -" + method + "cor -selname," +var1 + " " + ff + " -selname," + var2 + " " + ff + " " + target
        target = run_cdo(cdo_command, target)

        new_files.append(target)
        new_commands.append(cdo_command)

    # update the state of the dataset
    self.history+=new_commands
    self._hold_history = copy.deepcopy(self.history)

    for ff in self:
        if ff in nc_safe:
            nc_safe.remove(ff)

    self.current = new_files

    # add the new file to the safe list
    for ff in self:
        nc_safe.append(ff)

    # tidy up the attributes of the netcdf file in the dataset
    self.rename({var1:"cor"})
    self.set_units({"cor":"-"})
    self.set_longnames({"cor":"Correlation between " + var1 +  " & " + var2})

    cleanup()
    self.disk_clean()



def cor_space(self, var1 = None, var2 = None):
    """
    Calculate the correlation correct between two variables in space, and for each time step. The correlation coefficient coefficient is calculated using values in all grid cells.

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable
    """

    return cor(self, var1 = var1, var2 = var2,   method = "fld")

def cor_time(self, var1 = None, var2 = None):
    """
    Calculate the correlation correct in time between two variables. The correlation is calculated for each grid cell

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable
    """
    return cor(self, var1 = var1, var2 = var2, method = "tim")




