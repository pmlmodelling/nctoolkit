from .runthis import run_this
from .runthis import run_cdo
from .temp_file import temp_file
from .session import nc_safe
from .show import nc_variables
from .cleanup import cleanup
from .cleanup import disk_clean
from .session import session_info
import copy
import os

def arithall(self, stat = "divc", x = None):
    """Method to add, subtract etc. a constant from a dataset"""

    # create the system command and run it
    cdo_command = f"cdo -{stat},{x}"

    run_this(cdo_command, self,  output = "ensemble")


def operation(self, method = "mul", ff = None, var = None):
    """Method to add, subtract etc. a netcdf file from another one"""


    if ff is not None:
        if os.path.exists(ff) == False:
            raise ValueError(f"{ff} does not exist!")

    if var is not None:
        if type(var) is not str:
            raise TypeError("var supplied is not a string")
        if var not in nc_variables(ff):
            raise ValueError("var supplied is not available in the dataset")

    if ff is not None:
        nc_safe.append(ff)
        self._safe.append(ff)

    if len(self.history) == len(self._hold_history):

        for x in self:

        # check that the datasets can actually be worked with
            if var is None:
                if len(nc_variables(ff)) != len(nc_variables(x)) and len(nc_variables(ff)) != 1:
                    raise ValueError("Datasets have incompatible variable numbers for the operation!")

        prior_command = ""

    else:

        prior_command = self.history[-1].replace("cdo ", " ").replace("  ", " ")

    if var is None:
        if "infile09178" in prior_command:
            cdo_command = f"cdo -{method} {prior_command} {ff}"
        else:
            cdo_command = f"cdo -{method} {prior_command} infile09178 {ff}"
    else:
        if "infile09178" in prior_command:
            cdo_command = f"cdo -{method} {prior_command} -selname,{var} {ff}"
        else:
            cdo_command = f"cdo -{method} {prior_command} infile09178 -selname,{var} {ff}"

    if session_info["lazy"] == False:
        target = temp_file(".nc")
        cdo_command += cdo_command + " " + target
        run_cdo(cdo_command, target)
        self.history.append(cdo_command)
        self._hold_history = copy.deepcopy(self.history)

    else:
        if len(self.history) > len(self._hold_history):
            self.history[-1] = cdo_command
        else:
            self.history.append(cdo_command)



def multiply(self, x = None, var = None):
    """
    Multiply a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to multiply the dataset by
    var: str
        A variable in the x to multiply the dataset by
    """

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

    operation(self = self, method = "mul", ff = ff, var = var)


def subtract(self, x = None, var = None):
    """
    Subtract from a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to subtract from the dataset
    var: str
        A variable in the x to use for the operation
    """

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

    operation(self = self, method = "sub", ff = ff, var = var)


def add(self, x = None, var = None):
    """
    Add to a dataset
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to add to the dataset
    var: str
        A variable in the x to use for the operation
    """

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

    operation(self = self, method = "add", ff = ff, var = var)



def divide(self, x = None, var = None):
    """
    Divide the data in the current dataset by the data in another dataset or netcdf file
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to divide the dataset by
    var: str
        A variable in the x to use for the operation
    """

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

    operation(self = self, method = "div", ff = ff, var = var)




