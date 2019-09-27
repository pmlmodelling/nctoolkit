import os
import copy
import tempfile
import multiprocessing

from ._filetracker import nc_created
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
import copy

def run_it(command, target):
    os.system(command)
    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")
    return target

def cor_space(self, var1 = None, var2 = None,  silent = False, cores = 1):
    """
    Method to calculate the correlation between two variables in space
    """

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
    split_base = tempfile.NamedTemporaryFile().name 
    split_base = split_base.replace("tmp/", "tmp/nchack")

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

    target = tempfile.NamedTemporaryFile().name  + ".nc"
    target = target.replace("tmp/", "tmp/nchack")
    nc_created.append(target)

    cdo_command = "cdo fldcor " + out1 + " " + out2 + " " + target
    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target) == False:
        raise ValueError("Calculating the correlation coefficient failed!")

    target1 = tempfile.NamedTemporaryFile().name  + ".nc"
    target1 = target1.replace("tmp/", "tmp/nchack")
    nc_created.append(target1)

    cdo_command = "cdo setname," + "cor " + target + " " + target1
    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target1) == False:
        raise ValueError("Changing the name to cor failed!")

    target2 = tempfile.NamedTemporaryFile().name  + ".nc"
    target2 = target2.replace("tmp/", "tmp/nchack")
    nc_created.append(target2)

    cdo_command = "cdo setunit," + "'' " + target1 + " " + target2
    new_self.history.append(cdo_command)
    os.system(cdo_command)

    if os.path.exists(target2) == False:
        raise ValueError("Changing the unit of cor failed!")

    new_self.current = target2

    new_self.set_longname({"cor":"Correlation between " + var1 +  " & " + var2})


    return new_self




