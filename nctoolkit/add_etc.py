import copy
import os
import subprocess
import warnings
import pandas as pd

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.session import nc_safe, session_info, append_safe, remove_safe
from nctoolkit.show import nc_variables, nc_years, nc_months, nc_times
from nctoolkit.temp_file import temp_file
from nctoolkit.utils import cdo_version, version_above


def arithall(self, stat="divc", x=None):
    """
    Method to add, subtract etc. a constant from a dataset
    This is used by add etc.
    """

    if len(self) == 0:
        raise ValueError("This does not work on empty datasets!")

    # create the system command and run it
    cdo_command = f"cdo -{stat},{x}"

    run_this(cdo_command, self, output="ensemble")


def operation(self, method="mul", ff=None, var=None):
    """
    Method to add, subtract etc. a netCDF file from another one
    This is used by add etc.
    """

    new = False

    if version_above(cdo_version(), "1.9.9"):
        new = True
    else:
        warnings.warn("Use CDO>=1.9.9 for more smarter operations")

    if new:

        self1 = self.copy()

        if len(self1) == 0:
            raise ValueError("This does not work on empty datasets!")

        # If the dataset has to be merged,
        # then this operation will not work without running it first
        self1.run()

        # throw error if the file to operate with does not exist
        if ff is not None:
            if os.path.exists(ff) is False:
                raise ValueError(f"{ff} does not exist!")

        ff_times = nc_times(ff)
        ff_times_df = pd.DataFrame({"time":ff_times}).assign(year = lambda x: x.time.dt.year, month = lambda x: x.time.dt.month, day = lambda x: x.time.dt.day).drop(columns = "time")

        # work out if it's a yearmon method

        op_method = None

        if len(ff_times_df) > 1:
            if len(ff_times_df) == len(ff_times_df.drop_duplicates()):
                if len(ff_times_df) > len(ff_times_df.loc[:,["year", "month"]].drop_duplicates()):
                    if len(ff_times_df) == len(ff_times_df.loc[:,["year", "month", "day"]].drop_duplicates()):
                        op_method = "yday"

        if len(ff_times_df) > 1:
            if len(ff_times_df) == len(ff_times_df.drop(columns = "day").drop_duplicates()):
                if len(set(ff_times_df.year)) > 1:
                    if len(set(ff_times_df.month)) > 1:
                        op_method = "yearmon"

        if len(ff_times_df) > 1:
            if len(ff_times_df) == len(ff_times_df.drop(columns = "day").drop_duplicates()):
                if len(set(ff_times_df.year)) == 1:
                    if len(set(ff_times_df.month)) > 1:
                        op_method = "mon"

        if len(ff_times_df) > 1:
            if len(ff_times_df) == len(ff_times_df.drop(columns = "day").drop_duplicates()):
                if len(set(ff_times_df.year)) > 1:
                    if len(set(ff_times_df.year)) == len(ff_times_df): 
                        op_method = "year"

        if len(ff_times_df) == 1:
            op_method = "single"


        # throw error if there is a problem with var
        if var is not None:
            if type(var) is not str:
                raise TypeError("var supplied is not a string")
            if var not in nc_variables(ff):
                raise ValueError("var supplied is not available in the dataset")

        bad_vars = False

        for x in self1:
            n_vars = len(nc_variables(ff))
            x_vars = len(nc_variables(x))

            if n_vars > x_vars:
                raise ValueError("Incompatible number of variables in datasets!")

            if n_vars != x_vars:
                if n_vars > 1:
                    raise ValueError("Incompatible number of variables in datasets!")

        self1.run()
        # leap years are tricky....

        # throw an error if things are ambiguous

        merge_names = False

        if len(self1) == 1:
            if len(self1.variables) > len(nc_variables(ff)):
                merge_names = True

        if merge_names:
            self1.split("variable")

        if method == "mul":
            nc_operation = "multiplication"
            nc_str = "Multiplying by a"
        if method == "sub":
            nc_operation = "subtraction"
            nc_str = "Subtracting a"
        if method == "add":
            nc_operation = "addition"
            nc_str = "Adding a"
        if method == "div":
            nc_operation = "division"
            nc_str = "Dividing by a"

        if op_method == "yday":
            for file in self1:
                file_times = nc_times(file)
                if len([x for x in file_times if "-02-29" in str(x)]) > 0:
                    raise ValueError("Dataset contains leap years, so the operation is ambiguous. Consider removing 29th February!")
                df_times = pd.DataFrame({"year":[x.year for x in file_times], "month":[x.month for x in file_times], "day": [x.day for x in file_times]}).drop_duplicates()

                for yy in df_times.year:
                    if len(df_times.query("year == @yy").merge(ff_times_df)) != len(ff_times_df):
                        raise ValueError(f"Time steps for the datasets/files are not compatible for the {nc_operation} method")
                    if len(df_times.query("year == @yy").merge(ff_times_df)) != len(df_times.query("year == @yy")):
                        raise ValueError(f"Time steps for the datasets/files are not compatible for the {nc_operation} method")

        if op_method == "year":
            for file in self1:
                ff_years = list(set([x.year for x in ff_times]))
                file_times = nc_times(file)
                file_years = list(set([x.year for x in file_times]))

                if ff_years != file_years:
                    raise ValueError("Years in datasets/files are not identical!")

        if method == "mul":
            nc_operation = "multiply"
        if method == "sub":
            nc_operation = "subtract"
        if method == "add":
            nc_operation = "add"
        if method == "div":
            nc_operation = "divide"

        new_commands = []
        new_files = []

        for x in self1:

            run = False

            if op_method == "single" and run == False:
                run = True
                if len(ff_times_df) == 1:
                    warnings.warn(f"{nc_str} single time step time series")

                if len(ff_times_df) == len(nc_times(x)):

                    warnings.warn(f"{nc_str} time series with the same number of time steps")

                if len(nc_times(x)) < len(nc_times(ff)):
                    warnings.warn(
                        f"Warning: Files do not have the same number of time steps. Only matching time steps used by {nc_operation}."
                    )
                if var is not None:
                    cdo_command = f"cdo -{method} {x} -selname,{var} {ff}"
                else:
                    cdo_command = f"cdo -{method} {x} {ff}"

                target = temp_file(".nc")
                cdo_command = f"{cdo_command} {target}"
                target = run_cdo(cdo_command, target, precision=self1._precision)
                new_files.append(target)
                new_commands.append(cdo_command)

            if op_method == "yday" and run == False:
                if var is not None:
                    cdo_command = f"cdo -yday{method} {x} -selname,{var} {ff}"
                else:
                    cdo_command = f"cdo -yday{method} {x} {ff}"
                run = True
                target = temp_file(".nc")
                cdo_command = f"{cdo_command} {target}"
                target = run_cdo(cdo_command, target, precision=self1._precision)
                new_files.append(target)
                new_commands.append(cdo_command)
                warnings.warn(f"{nc_str} daily time series")

            if op_method == "yearmon" and run == False:
                if var is not None:
                    cdo_command = f"cdo -mon{method} {x} -selname,{var} {ff}"
                else:
                    cdo_command = f"cdo -mon{method} {x} {ff}"
                run = True
                target = temp_file(".nc")
                cdo_command = f"{cdo_command} {target}"
                target = run_cdo(cdo_command, target, precision=self1._precision)
                new_files.append(target)
                new_commands.append(cdo_command)

            ## monthly time series

            if op_method == "mon" and run == False:
               run = True

               if bad_vars:
                   raise ValueError(
                       "Datasets/files do not have the same number of variables!"
                   )
               if var is not None:
                   cdo_command = f"cdo -ymon{method} {x} -selname,{var} {ff}"
               else:
                   cdo_command = f"cdo -ymon{method} {x} {ff}"

               target = temp_file(".nc")
               cdo_command = f"{cdo_command} {target}"
               target = run_cdo(cdo_command, target, precision=self1._precision)
               new_files.append(target)
               new_commands.append(cdo_command)
               warnings.warn(f"{nc_str} monthly time series")
            ## yearly time series

            if op_method == "year" and run == False:  
                run = True
                if var is not None:
                    cdo_command = f"cdo -year{method} {x} -selname,{var} {ff}"
                else:
                    cdo_command = f"cdo -year{method} {x} {ff}"
                target = temp_file(".nc")
                cdo_command = f"{cdo_command} {target}"
                target = run_cdo(cdo_command, target, precision=self1._precision)
                new_files.append(target)
                new_commands.append(cdo_command)
                warnings.warn(f"{nc_str} yearly time series")


            if len(nc_years(ff)) == 1 and run is False:
                if (len(nc_times(x)) / len(nc_years(x))) == len(nc_times(ff)):
                    run = True

                    if (nc_years(ff) == nc_years(x)) or (
                        len(nc_times(ff)) == len(nc_times(x))
                    ):

                        if len(ff_times_df) == 1:
                            warnings.warn(f"{nc_str} single time step time series")

                        if len(ff_times_df) == len(nc_times(x)):

                            warnings.warn(f"{nc_str} time series with the same number of time steps")

                        if len(nc_times(x)) < len(nc_times(ff)):
                            warnings.warn(
                                f"Warning: Files do not have the same number of time steps. Only matching time steps used by {nc_operation}."
                            )
                        if var is not None:
                            cdo_command = f"cdo -{method} {x} -selname,{var} {ff}"
                        else:
                            cdo_command = f"cdo -{method} {x} {ff}"

                        target = temp_file(".nc")
                        cdo_command = f"{cdo_command} {target}"
                        target = run_cdo(cdo_command, target, precision=self1._precision)
                        new_files.append(target)
                        new_commands.append(cdo_command)
                    else:
                        if var is not None:
                            cdo_command = f"cdo -yday{method} {x} -selname,{var} {ff}"
                        else:
                            cdo_command = f"cdo -yday{method} {x} {ff}"
                        target = temp_file(".nc")
                        cdo_command = f"{cdo_command} {target}"
                        target = run_cdo(cdo_command, target, precision=self1._precision)
                        new_files.append(target)
                        new_commands.append(cdo_command)


            if run is False:
                if len(nc_times(x)) < len(nc_times(ff)):
                    warnings.warn(
                        f"Warning: Files do not have the same number of time steps. Only matching time steps used by {nc_operation}."
                    )

                if len(nc_times(x)) != len(nc_times(ff)) and len(nc_times(ff)) > 1:
                    raise ValueError(
                        f"Time steps in datasets are not compatible for {nc_operation} method! Operations require yearly/monthly or daily time series"
                    )

                run = True

                if var is not None:
                    cdo_command = f"cdo -{method} {x} -selname,{var} {ff}"
                else:
                    cdo_command = f"cdo -{method} {x} {ff}"
                target = temp_file(".nc")
                cdo_command = f"{cdo_command} {target}"
                target = run_cdo(cdo_command, target, precision=self1._precision)
                new_files.append(target)
                new_commands.append(cdo_command)
                warnings.warn(f"{nc_str} single time step time series")

        if run is False:
            raise ValueError(
                f"nctoolkit cannot automatically determine {nc_operation} method for the dataset timesteps given!"
            )

        if len(new_commands) > 0:
            for cc in new_commands:
                self1.history.append(cc.replace("  ", " "))

            self1.current = new_files

            for ff in new_files:
                remove_safe(ff)
            self1._hold_history = copy.deepcopy(self1.history)

            if merge_names:
                self1.merge()
                self1.run()
            cleanup()

            self.history = self1.history
            self._hold_history = self1._hold_history
            self.current = self1.current

            return None

    if new == False:

        # make sure the ff file is not removed from safe list in subsequent
        # actions prior to running
        if (ff is not None) and (session_info["lazy"]):
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

        if session_info["lazy"] is False:

            new_files = []
            new_commands = []

            for FF in self:

                target = temp_file(".nc")
                the_command = cdo_command.replace("infile09178", FF) + " " + target
                the_command = tidy_command(the_command)
                target = run_cdo(the_command, target, precision=self._precision)
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
            raise ValueError("This can only work with single file datasets")
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
            raise ValueError("This can only work with single file datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="sub", ff=ff, var=var)


def add(self, x=None, var=None):
    """
    Add to a dataset
    This will add a constant, another dataset or a netCDF file to the dataset. 
    nctoolkit will automatically determine the appropriate comparison required.

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
            raise ValueError("This can only work with single variable datasets")
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
            raise ValueError("This can only work with single file datasets")
    else:
        ff = x

    if type(ff) is not str:
        raise TypeError("You have not provided an int, float, dataset or file path!")

    operation(self=self, method="div", ff=ff, var=var)


def abs(self):
    """
    Method to get the absolute value of variables

    Examples
    ------------

    If you wanted to get the absolute value of each variable, you just need do this:

    >>> ds.abs()

    """
    cdo_command = f"cdo -abs"

    run_this(cdo_command, self, output="ensemble")


def power(self, x=None):
    """
    Powers of variables in dataset
    Parameters
    ------------
    x: int, float
        An int or float to take the variables to the power of

    Examples
    ------------

    If you wanted to take each variable to the power of 0.5 you would do this:

    >>> ds.power(0.5)

    """

    if type(x) is not float and type(x) is not int:
        raise TypeError("x is not a float or int")

    cdo_command = f"cdo -pow,{x}"

    run_this(cdo_command, self, output="ensemble")


def exp(self):
    """
    Method to get the exponential of variables

    Examples
    ------------

    If you wanted to calculate the exponential of a variable, you just need to do this:

    >>> ds.exp(0.5)

    """
    cdo_command = f"cdo -exp"

    run_this(cdo_command, self, output="ensemble")


def log(self):
    """
    Method to get the natural log of variables

    Examples
    ------------

    If you wanted to calculate the natural log of each variable, you just need to do this:

    >>> ds.log()

    """
    cdo_command = f"cdo -ln"

    run_this(cdo_command, self, output="ensemble")


def log10(self):
    """
    Method to get the base 10 log of variables

    Examples
    ------------

    If you wanted to calculate the base 10 log of each variable, you just need to do this:

    >>> ds.log10()

    """
    cdo_command = f"cdo -log10"

    run_this(cdo_command, self, output="ensemble")


def square(self):
    """
    Method to get the square of variables

    Examples
    ------------

    If you wanted to calculate the square of each variable, you just need to do this:

    >>> ds.power()

    """
    cdo_command = f"cdo -sqr"

    run_this(cdo_command, self, output="ensemble")


def sqrt(self):
    """
    Method to get the square root of variables

    Examples
    ------------

    If you wanted to calculate the square root of each variable, you just need to do this:

    >>> ds.sqrt()

    """
    cdo_command = f"cdo -sqrt"

    run_this(cdo_command, self, output="ensemble")
