import os
import copy
import multiprocessing

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
import copy


def cor(self, var1 = None, var2 = None, method = "fld"):

    new_self = copy.deepcopy(self)

    if var1 is None or var2 is None:
        raise ValueError("Both variables are not given")


    # First step is to check if the current file exists
    if type(self.current) is str:
        if os.path.exists(self.current) == False:
            raise ValueError("The file " + self.current + " does not exist!")
    else:
        raise ValueError("This method only works on single files")

    # We need to split the file by name
    split_base = temp_file()

    vars = [var1, var2]
    vars = str_flatten(vars)
    self.select_variables(vars = vars)

    # we now need to split up the file by variable
    
    out1 = split_base + var1 + ".nc"
    out2 = split_base + var2 + ".nc"
    nc_created.append(out1)
    nc_created.append(out2)

    cdo_command = "cdo splitname " + self.current + " " + split_base

    new_self.history.append(cdo_command)

    os.system(cdo_command)

    if os.path.exists(out1) == False or os.path.exists(out2) == False:
        raise ValueError("Splitting the file by name did not work!")

    target = temp_file(".nc")
    nc_created.append(target)

    cdo_command = "cdo " + method + "cor " + out1 + " " + out2 + " " + target

    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target) == False:
        raise ValueError("Calculating the correlation coefficient failed!")

    target1 = temp_file(".nc")
    nc_created.append(target1)

    cdo_command = "cdo setname," + "cor " + target + " " + target1
    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target1) == False:
        raise ValueError("Changing the name to cor failed!")

    target2 = temp_file(".nc")
    nc_created.append(target2)

    cdo_command = "cdo setunit," + "'-' " + target1 + " " + target2
    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target2) == False:
        raise ValueError("Changing the unit of cor failed!")

    new_self.current = target2

    new_self.set_longname({"cor":"Correlation between " + var1 +  " & " + var2})


    return new_self




def cor_space(self, var1 = None, var2 = None):
    """
    Calculate the correlation correct between two variables in space, and for each time step

    Parameters
    -------------
    var1: str
        The first variable 
    var2: str
        The  second variable

    Returns
    -------------
    nchack.DataSet
        Data set with the correlation coefficients 
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

    Returns
    -------------
    nchack.DataSet
        Data set with the correlation coefficients 
    """
    return cor(self, var1 = var1, var2 = var2, method = "tim")




