from .runthis import run_this
from .runthis import run_cdo
from .temp_file import temp_file
from .flatten import str_flatten
from .session import nc_safe
from .show import nc_variables
from .session import session_info
import subprocess
import copy

def arithall(self, stat = "divc", x = None):
    """Method to add, subtract etc. a constant from a dataset"""

    # create the system command and run it
    cdo_command = "cdo -" + stat + "," + str(x)

    run_this(cdo_command, self,  output = "ensemble")


def operation(self, method = "mul", ff = None):
    """Method to add, subtract etc. a netcdf file from another one"""

    if type(self.current) is list:
        raise TypeError("This only works for single files presently")

    self.release()

    # check that the datasets can actually be worked with
    if len(nc_variables(ff)) != len(nc_variables(self.current)) and len(nc_variables(ff)) != 1:
        raise ValueError("Datasets have incompatible variable numbers for the operation!")

    # create the temp file
    target = temp_file(".nc")

    # create the system call
    cdo_command = "cdo -L " + method + " "  + self.current + " " + ff + " " + target

    # modify system call if threadsafe
    if session_info["thread_safe"]:
        cdo_command = cdo.command.replace("-L ", " ")

    # run the system call
    target = run_cdo(cdo_command, target)

    # update the history etc.
    self.history.append(cdo_command)
    self._hold_history = copy.deepcopy(self.history)
    nc_safe.remove(self.current)
    self.current = target
    nc_safe.append(self.current)



def multiply(self, x = None):
    """
    Multiply a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float single file dataset or netcdf file to multiply the dataset by
    """
    self.release()

    # 1: int, float multiplication
    if isinstance(x, (int, float)):
        return arithall(self, stat = "mulc", x = x)

    # 2: dataset or netcdf file multiplication
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.release()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self = self, method = "mul", ff = ff)


def subtract(self, x = None):
    """
    Subtract from a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float single file dataset or netcdf file to subtract from the dataset
    """

    self.release()

    # 1: int, float subtraction
    if isinstance(x, (int, float)):
        return arithall(self, stat = "subc", x = x)

    # 2: dataset or netcdf file subtraction
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.release()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self = self, method = "sub", ff = ff)


def add(self, x = None):
    """
    Add to a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float single file dataset or netcdf file to add to the dataset
    """

    self.release()

    # 1: int, float addition
    if isinstance(x, (int, float)):
        return arithall(self, stat = "addc", x = x)

    # 2: dataset or netcdf file addition
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.release()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self = self, method = "add", ff = ff)



def divide(self, x = None):
    """
    Divide the data in the current dataset by the data in another dataset or netcdf file
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float single file dataset or netcdf file to divide the dataset by
    """

    self.release()

    # 1: int, float division
    if isinstance(x, (int, float)):
        return arithall(self, stat = "divc", x = x)

    # 2: dataset or netcdf file division
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.release()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self = self, method = "div", ff = ff)




