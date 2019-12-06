from .runthis import run_this
from .runthis import run_cdo
from .temp_file import temp_file
from .flatten import str_flatten
from .session import nc_safe
from .show import nc_variables
import subprocess
import copy

def arithall(self, stat = "divc", x = None):
    """Method to calculate the spatial stat from a netcdf"""

    cdo_command = "cdo -" + stat + "," + str(x)

    run_this(cdo_command, self,  output = "ensemble")


def operation(self, method = "mul", ff = None):

    if type(self.current) is list:
        raise TypeError("This only works for single files presently")

    self.release()

    if len(nc_variables(ff)) > 1:
        raise ValueError("Check dataset or file you are using. It had more than one variables")

    target = temp_file(".nc")
    cdo_command = "cdo -L " + method + " "  + self.current + " " + ff + " " + target
    target = run_cdo(cdo_command, target)
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
    if isinstance(x, (int, float)):
        return arithall(self, stat = "mulc", x = x)

    self.release()

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

    if isinstance(x, (int, float)):
        return arithall(self, stat = "subc", x = x)

    self.release()

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

    if isinstance(x, (int, float)):
        return arithall(self, stat = "addc", x = x)
    self.release()

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

    if isinstance(x, (int, float)):
        return arithall(self, stat = "divc", x = x)

    self.release()

    if "api.DataSet" in str(type(x)):
        x.release()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self = self, method = "div", ff = ff)




