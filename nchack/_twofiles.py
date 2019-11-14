from ._runthis import run_this
from ._runthis import run_cdo
from ._temp_file import temp_file
from .flatten import str_flatten
from ._session import nc_safe 
import subprocess
import copy

def operation(self, method = "mul", ff = None,  cores = 1):

    if type(self.current) is list:
        raise ValueError("This only works for single files presently")

    if self.run == False:
        self.release()


    target = temp_file(".nc")
    cdo_command = "cdo -L " + method + " "  + self.current + " " + ff + " " + target
    target = run_cdo(cdo_command, target)
    self.history.append(cdo_command)
    self.hold_history = copy.deepcopy(self.history)
    nc_safe.remove(self.current)
    self.current = target
    nc_safe.append(self.current)



def multiply(self, second = None, cores = 1):
    """
    Multiply a dataset by another dataset or netcdf file
    Parameters
    ------------
    second: DataSet or netcdf file
        A dataset or netcdf file to multiply the current dataset by.
    cores: int
        The number of cores to use
    """

    if "api.DataSet" in str(type(second)):
        ff = second.current
    else:
        ff = second

    if type(ff) is not str:
        raise ValueError("second must be a file path")

    operation(self = self, method = "mul", ff = ff, cores = cores)


def subtract(self, second = None, cores = 1):
    """
    Subtract the data from another dataset or netcdf from the current dataset
    Parameters
    ------------
    second: DataSet or netcdf file
        A dataset or netcdf file to substract from the current dataset by
    cores: int
        The number of cores to use
    """
    if "api.DataSet" in str(type(second)):
        ff = second.current
    else:
        ff = second

    if type(ff) is not str:
        raise ValueError("second must be a file path")

    operation(self = self, method = "sub", ff = ff, cores = cores)

 
def add(self, second = None, cores = 1):
    """
    Add the data from another dataset or netcdf to the current dataset
    Parameters
    ------------
    second: DataSet or netcdf file
        A dataset or netcdf file to add to the current dataset by
    cores: int
        The number of cores to use
    """

    if "api.DataSet" in str(type(second)):
        ff = second.current
    else:
        ff = second

    if type(ff) is not str:
        raise ValueError("second must be a file path")

    operation(self = self, method = "add", ff = ff, cores = cores)


 
def divide(self, second = None, cores = 1):
    """
    Divide the data in the current dataset by the data in another dataset or netcdf file
    Parameters
    ------------
    second: DataSet or netcdf file
        A dataset or netcdf file to divide the current dataset by
    cores: int
        The number of cores to use
    """

    if "api.DataSet" in str(type(second)):
        ff = second.current
    else:
        ff = second

    if type(ff) is not str:
        raise ValueError("second must be a file path")

    operation(self = self, method = "divide", ff = ff, cores = cores)


