
import copy
import os
import subprocess

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.session import nc_safe, session_info
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file


def arithall(self, stat="divc", x=None):
    """
    Method to add, subtract etc. a constant from a dataset
    This is used by add etc.
    """

    # create the system command and run it
    cdo_command = f"cdo -{stat},{x}"

    run_this(cdo_command, self, output="ensemble")


def operation(self, method="mul", ff=None, var=None):
    """
    Method to add, subtract etc. a netcdf file from another one
    This is used by add etc.
    """

    # get the cdo version
    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]

    # If the dataset has to be merged, then this operation will not work without running it first
    if self._merged:
        self.run()

    # throw error if the file to operate with does not exist
    if ff is not None:
        if os.path.exists(ff) == False:
            raise ValueError(f"{ff} does not exist!")

    # throw error if there is a problem with var
    if var is not None:
        if type(var) is not str:
            raise TypeError("var supplied is not a string")
        if var not in nc_variables(ff):
            raise ValueError("var supplied is not available in the dataset")

    # make sure the ff file is not removed from safe list in subsequent actions prior to running
    if (ff is not None) and (session_info["lazy"]):
        nc_safe.append(ff)
        self._safe.append(ff)

    if len(self.history) == len(self._hold_history):

        for x in self:

            # check that the datasets can actually be worked with
            if var is None:
                if (len(nc_variables(ff)) != len(nc_variables(x))) and (
                    len(nc_variables(ff)) != 1
                ):
                    raise ValueError(
                        "Datasets have incompatible variable numbers for the operation!"
                    )

        prior_command = ""

    else:

        prior_command = self.history[-1].replace("cdo ", " ").replace("  ", " ")

    # we need to make sure you can chain multiple adds etc.#
    # the approach below will work, but can probably be improved on

    if var is None:
        if "infile09178" in prior_command:
            cdo_command = f"cdo -{method} {prior_command} {ff}"
        else:
            cdo_command = f"cdo -{method} {prior_command} infile09178 {ff}"
    else:
        if "infile09178" in prior_command:
            cdo_command = f"cdo -{method} {prior_command} -selname,{var} {ff}"
        else:
            cdo_command = (
                f"cdo -{method} {prior_command} infile09178 -selname,{var} {ff}"
            )

    # run the command if not lazy

    if (session_info["lazy"] == False) or (cdo_version in ["1.9.3"]):

        new_files = []
        new_commands = []

        for FF in self:

            target = temp_file(".nc")
            the_command = cdo_command.replace("infile09178", FF) + " " + target
            the_command = tidy_command(the_command)
            target = run_cdo(the_command, target)
            new_files.append(target)
            new_commands.append(the_command)

        for cc in new_commands:
            self.history.append(cc.replace("  ", " "))

        self.current = new_files
        self._hold_history = copy.deepcopy(self.history)
        for rr in self._safe:
            nc_safe.remove(ff)
        self._safe = []
        cleanup()

    # update history if lazy
    else:
        if len(self.history) > len(self._hold_history):
            self.history[-1] = cdo_command
        else:
            self.history.append(cdo_command)

    cleanup()


def multiply(self, x=None, var=None):
    """
    Multiply a dataset
    This will multiply a dataset by a constant, another dataset or a NetCDF file.
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to multiply the dataset by. If multiplying by a dataset or single file there must only be a single variable in it, unless var is supplied. The grids must be the same.
    var: str
        A variable in the x to multiply the dataset by
    """

    # 1: int, float multiplication
    if isinstance(x, (int, float)):
        arithall(self, stat="mulc", x=x)
        return None

    # 2: dataset or netcdf file multiplication
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="mul", ff=ff, var=var)


def subtract(self, x=None, var=None):
    """
    Subtract from a dataset
    This will subtract a constant, another dataset or a NetCDF file from the dataset.
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to subtract from the dataset. If a dataset or netcdf is supplied this must only have one variable, unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation
    """

    # 1: int, float subtraction
    if isinstance(x, (int, float)):
        arithall(self, stat="subc", x=x)
        return None

    # 2: dataset or netcdf file subtraction
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="sub", ff=ff, var=var)


def add(self, x=None, var=None):
    """
    Add to a dataset
    This will add a constant, another dataset or a NetCDF file to the dataset.
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to add to the dataset. If a dataset or netcdf file is supplied, this must have only one variable, unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation
    """

    # 1: int, float addition
    if isinstance(x, (int, float)):
        arithall(self, stat="addc", x=x)
        return None

    # 2: dataset or netcdf file addition
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="add", ff=ff, var=var)


def divide(self, x=None, var=None):
    """
    Divide the data
    This will divide the dataset by a constant, another dataset or a NetCDF file.
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to divide the dataset by. If a dataset or netcdf file is supplied, this must have only one variable, unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation
    """

    # 1: int, float division
    if isinstance(x, (int, float)):
        arithall(self, stat="divc", x=x)
        return None

    # 2: dataset or netcdf file division
    # get the netcdf file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        ff = x.current
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="div", ff=ff, var=var)
