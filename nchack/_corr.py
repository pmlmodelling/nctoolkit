import os
import copy
import multiprocessing

from ._temp_file import temp_file
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
from ._session import nc_safe
from ._runthis import run_cdo

import copy


def cor(self, var1 = None, var2 = None, method = "fld"):

    if var1 is None or var2 is None:
        raise ValueError("Both variables are not given")

    # First step is to check if the current file exists
    if type(self.current) is str:
        if os.path.exists(self.current) == False:
            raise ValueError("The file " + self.current + " does not exist!")
    else:
        raise ValueError("This method only works on single files")


    if self.run == False:
        self.release()

    target = temp_file(".nc")

    cdo_command = "cdo -L -" + method + "cor -selname," +var1 + " " + self.current + " -selname," + var2 + " " + self.current + " " + target
    target = run_cdo(cdo_command, target)

    self.history.append(cdo_command)
    self.current = target

    self.rename({var1:"cor"})
    self.set_unit({"cor":"-"})

    self.set_longname({"cor":"Correlation between " + var1 +  " & " + var2})



def cor_space(self, var1 = None, var2 = None):
    """
    Calculate the correlation correct between two variables in space, and for each time step

    Parameters
    -------------
    var1: str
        The first variable 
    var2: str
        The  second variable

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
        The  second variable

    """
    return cor(self, var1 = var1, var2 = var2, method = "tim")




