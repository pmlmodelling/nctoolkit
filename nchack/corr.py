import os
import copy
import multiprocessing

from .temp_file import temp_file
from .flatten import str_flatten
from .select import select_variables
from .setters import set_longnames
from .session import nc_safe
from .runthis import run_cdo
from .cleanup import cleanup

import copy


def cor(self, var1 = None, var2 = None, method = "fld"):

    if var1 is None or var2 is None:
        raise ValueError("Both variables are not given")

    # First step is to check if the current file exists
    if type(self.current) is not str:
        raise ValueError("This method only works on single files")

    # make sure everything has been evaluated
    self.release()

    # create the temp file for targeting
    target = temp_file(".nc")

    # check that the variables selected are actually in the dataset
    variables = self.variables
    if var1 not in variables:
        raise ValueError(var1 + " is not available in the DataSet")
    if var2 not in variables:
        raise ValueError(var2 + " is not available in the DataSet")

    # create the cdo command and run it
    cdo_command = "cdo -L -" + method + "cor -selname," +var1 + " " + self.current + " -selname," + var2 + " " + self.current + " " + target
    target = run_cdo(cdo_command, target)

    # update the state of the dataset
    self.history.append(cdo_command)
    self._hold_history = copy.deepcopy(self.history)
    self.current = target

    # add the new file to the safe list
    nc_safe.append(self.current)

    # tidy up the attributes of the netcdf file in the dataset
    self.rename({var1:"cor"})
    self.set_units({"cor":"-"})
    self.set_longnames({"cor":"Correlation between " + var1 +  " & " + var2})

    cleanup()



def cor_space(self, var1 = None, var2 = None):
    """
    Calculate the correlation correct between two variables in space, and for each time step

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
    Calculate the correlation correct in time between two variables, for each grid cell

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable
    """
    return cor(self, var1 = var1, var2 = var2, method = "tim")




