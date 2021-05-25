import copy
import os
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.session import nc_safe, session_info, append_safe, remove_safe
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file
from nctoolkit.utils import cdo_version



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
    Method to add, subtract etc. a netCDF file from another one
    This is used by add etc.
    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    # If the dataset has to be merged,
    # then this operation will not work without running it first
    if self._merged:
        self.run()

    # throw error if the file to operate with does not exist
    if ff is not None:
        if os.path.exists(ff) is False:
            raise ValueError(f"{ff} does not exist!")

    # throw error if there is a problem with var
    if var is not None:
        if type(var) is not str:
            raise TypeError("var supplied is not a string")
        if var not in nc_variables(ff):
            raise ValueError("var supplied is not available in the dataset")

    # make sure the ff file is not removed from safe list in subsequent
    # actions prior to running
    if (ff is not None) and (session_info["lazy"]) :
        append_safe(ff)
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

    if (session_info["lazy"] is False):

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

        for ff in new_files:
            remove_safe(ff)
        self._hold_history = copy.deepcopy(self.history)
        cleanup()

    # update history if lazy
    else:
        if len(self.history) > len(self._hold_history):
            self.history[-1] = cdo_command
        else:
            self.history.append(cdo_command)

    # remove anything from self._safe if it was ever set up

    cleanup()


def multiply(self, x=None, var=None):
    """
    Multiply a dataset
    This will multiply a dataset by a constant, another dataset or a netCDF file.
    Parameters
    ------------
    x: int, float, DataSet or netCDF file
        An int, float, single file dataset or netCDF file to multiply the dataset by.
        If multiplying by a dataset or single file there must only be a single variable
        in it, unless var is supplied. The grids must be the same.
    var: str
        A variable in the x to multiply the dataset by

    Examples
    ------------

    If you wanted to multiply variables in a dataset by 10, you would do the following:

    >>> ds.multiply(10)

    To multiply the values in a dataset by the values of variables in dataset ds2, you would do the following:

    >>> ds1.multiply(ds2)

    Grids in the datasets must match. Multiplication will occur in matching timesteps in ds1 and ds2. If there is only 1 timestep in ds2, then
    the data from that timestep in ds2 will multiply the data in all timesteps in ds1.

    Multiplying a dataset by the data from another netCDF file will work in the same way:

    >>> ds.multiply("example.nc")
    """

    # 1: int, float multiplication
    if isinstance(x, (int, float)):
        arithall(self, stat="mulc", x=x)
        return None

    # 2: dataset or netCDF file multiplication
    # get the netCDF file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) == 1:
            ff = x.current[0]
        else:
            raise TypeError("This can only work with single variable datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="mul", ff=ff, var=var)


def subtract(self, x=None, var=None):
    """
    Subtract from a dataset
    This will subtract a constant, another dataset or a netCDF file from the dataset.
    Parameters
    ------------
    x: int, float, DataSet or netCDF file
        An int, float, single file dataset or netCDF file to subtract from the dataset.
        If a dataset or netCDF is supplied this must only have one variable,
        unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation

    Examples
    ------------

    If you wanted to subtract 10 from all variables in a dataset, you would do the following:

    >>> ds.subtract(10)

    To substract the values in a dataset ds2 from those in a dataset ds1, you would do the following:

    >>> ds1.subtract(ds2)

    Grids in the datasets must match. Division will occur in matching timesteps in ds1 and ds2 if there are matching timesteps. If there is only 1 timestep in ds2, then
    the data from that timestep in ds2 will be subtracted from the data in all timesteps in ds1.

    Subtracting of the data from another netCDF file will work in the same way:

    >>> ds1.subtract("example.nc")
    """

    # 1: int, float subtraction
    if isinstance(x, (int, float)):
        arithall(self, stat="subc", x=x)
        return None

    # 2: dataset or netCDF file subtraction
    # get the netCDF file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) == 1:
            ff = x.current[0]
        else:
            raise TypeError("This can only work with single variable datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="sub", ff=ff, var=var)


def add(self, x=None, var=None):
    """
    Add to a dataset
    This will add a constant, another dataset or a netCDF file to the dataset.
    Parameters
    ------------
    x: int, float, DataSet or netCDF file
        An int, float, single file dataset or netCDF file to add to the dataset.
        If a dataset or netCDF file is supplied, this must have only one variable,
        unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation

    Examples
    ------------

    If you wanted to add 10 to all variables in a dataset, you would do the following:

    >>> ds.add(10)

    To add the values in a dataset ds2 from a dataset ds1, you would do the following:

    >>> ds1.add(ds2)

    Grids in the datasets must match. Addition will occur in matching timesteps in ds1 and ds2. If there is only 1 timestep in ds2, then
    the data from that timestep will be added to the data in all ds1 time steps.

    Adding the data from another netCDF file will work in the same way:

    >>> ds1.add("example.nc")


    """

    # 1: int, float addition
    if isinstance(x, (int, float)):
        arithall(self, stat="addc", x=x)
        return None

    # 2: dataset or netCDF file addition
    # get the netCDF file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) == 1:
            ff = x.current[0]
        else:
            raise TypeError("This can only work with single variable datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="add", ff=ff, var=var)


def divide(self, x=None, var=None):
    """
    Divide the data
    This will divide the dataset by a constant, another dataset or a netCDF file.
    Parameters
    ------------
    x: int, float, DataSet or netCDF file
        An int, float, single file dataset or netCDF file to divide the dataset by.
        If a dataset or netCDF file is supplied, this must have only one variable,
        unless var is provided. The grids must be the same.
    var: str
        A variable in the x to use for the operation

    Examples
    ------------

    If you wanted to dividie all variables in a dataset by 20, you would do the following:

    >>> ds.divide(10)

    To divide values in a dataset by those in the dataset ds2 from a dataset ds1, you would do the following:

    >>> ds1.divide(ds2)

    Grids in the datasets must match. Division will occur in matching timesteps in ds1 and ds2. If there is only 1 timestep in ds2, then
    the data from that timestep in ds2 will divided the data in all ds1 time steps.

    Adding the data from another netCDF file will work in the same way:

    >>> ds.divide("example.nc")
    """

    # 1: int, float division
    if isinstance(x, (int, float)):
        arithall(self, stat="divc", x=x)
        return None

    # 2: dataset or netCDF file division
    # get the netCDF file(s)
    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) == 1:
            ff = x.current[0]
        else:
            raise TypeError("This can only work with single variable datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="div", ff=ff, var=var)
