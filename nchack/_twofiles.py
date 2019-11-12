from ._runthis import run_this
from ._runthis import run_cdo
from ._temp_file import temp_file
from .flatten import str_flatten
from ._session import nc_safe 
import subprocess

def operation(self, method = "mul", ff = None,  cores = 1):

    if type(self.current) is list:
        raise ValueError("This only works for single files presently")


    target = temp_file(".nc")
    cdo_command = "cdo -L " + method + " "  + self.current + " " + ff + " " + target
    target = run_cdo(cdo_command, target)
    self.history.append(cdo_command)
    nc_safe.remove(self.current)
    self.current = target
    nc_safe.append(self.current)



def multiply(self, second = None, cores = 1):

    if "api.DataSet" in str(type(second)):
        ff = second.current
    else:
        ff = second

    if type(ff) is not str:
        raise ValueError("second must be a file path")

    operation(self = self, method = "mul", ff = ff, cores = cores)
