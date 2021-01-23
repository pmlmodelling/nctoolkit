
import copy
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_nco, tidy_command
from nctoolkit.temp_file import temp_file
from nctoolkit.session import nc_safe, remove_safe
from nctoolkit.time_stat import *
from nctoolkit.verticals import *
from nctoolkit.show import nc_variables
import warnings




#############################
# Delete these in March 2021
###########################
def var(self):
    """
    Calculate the temporal variance of all variables
    """
    warnings.warn(message = "var is now deprecated. Please use tvariance!")
    time_stat(self, stat="var")

def cum_sum(self):
    """
    Calculate the temporal cumulative sum of all variables
    """
    # create cdo command and runit
    warnings.warn(message = "cum_sum is now deprecated. Please use tcumsum!")
    time_stat(self, stat="cumsum")

def vertical_cum_sum(self):
    """
    Calculate the vertical sum of variable values
    This is calculated for each time step and grid cell
    """
    warnings.warn(message = "vertical_cum_sum is now deprecated. Please use vertical_cumsum!")
    vertstat(self, stat="cum")

def view(self):
    """
    Open the current dataset's file in ncview
    """
    warnings.warn(message = "view is now deprecated. Use plot instead!")
    self.run()

    if len(self) == 1:
        os.system("ncview " + self.current[0] + "&")
    else:
        print("You cannot send multiple files to ncview!")




def dailystat(self, stat="mean"):
    """Function to calculate the daily statistic for a function"""

    cdo_command = f"cdo -day{stat}"

    run_this(cdo_command, self, output="ensemble")


def daily_mean(self):
    """
    Calculate the daily mean for each variable
    """
    warnings.warn(message="Warning: daily_mean is deprecated. Use tmean!")
    dailystat(self, stat="mean")


def daily_min(self):
    """
    Calculate the daily minimum for each variable
    """
    warnings.warn(message="Warning: daily_min is deprecated. Use tmin!")
    dailystat(self, stat="min")


def daily_max(self):
    """
    Calculate the daily maximum for each variable
    """
    warnings.warn(message="Warning: daily_max is deprecated. Use tmax!")
    dailystat(self, stat="max")


def daily_range(self):
    """
    Calculate the daily range for each variable
    """
    warnings.warn(message="Warning: daily_range is deprecated. Use trange!")
    dailystat(self, stat="range")


def daily_sum(self):
    """
    Calculate the daily sum for each variable
    """
    warnings.warn(message="Warning: daily_sum is deprecated. Use tsum!")
    dailystat(self, stat="sum")

def ydaystat(self, stat="mean"):
    """
    Method to calculate daily climatologies
    """
    # create the cdo command and run it
    cdo_command = "cdo -yday" + stat
    run_this(cdo_command, self, output="ensemble")


def daily_mean_climatology(self):
    """
    Calculate a daily mean climatology
    """
    warnings.warn(message="Warning: daily_mean_climatology is deprecated. Use tmean!")
    ydaystat(self, stat="mean")


def daily_min_climatology(self):
    """
    Calculate a daily minimum climatology
    """
    warnings.warn(message="Warning: daily_min_climatology is deprecated. Use tmin!")
    ydaystat(self, stat="min")


def daily_max_climatology(self):
    """
    Calculate a daily maximum climatology
    """
    warnings.warn(message="Warning: daily_max_climatology is deprecated. Use tmax!")
    ydaystat(self, stat="max")


def daily_range_climatology(self):
    """
    Calculate a daily range climatology
    """
    warnings.warn(message="Warning: daily_range_climatology is deprecated. Use trange!")
    ydaystat(self, stat="range")


def monstat(self, stat="mean"):
    """Method to calculate the monthly statistic from a netcdf file"""
    cdo_command = f"cdo -mon{stat}"

    run_this(cdo_command, self, output="ensemble")


def monthly_mean(self):
    """
    Calculate the monthly mean for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_mean is deprecated. Use tmean!")
    monstat(self, stat="mean")


def monthly_min(self):
    """
    Calculate the monthly minimum for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_min is deprecated. Use tmin!")
    monstat(self, stat="min")


def monthly_max(self):
    """
    Calculate the monthly maximum for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_max is deprecated. Use tmax!")
    monstat(self, stat="max")


def monthly_range(self):
    """
    Calculate the monthly range for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_range is deprecated. Use trange!")
    monstat(self, stat="range")

def monthly_sum(self):
    """
    Calculate the monthly range for each year/month combination in files.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_sum is deprecated. Use tsum!")
    monstat(self, stat="sum")



def ymonstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -ymon{stat}"

    run_this(cdo_command, self, output="ensemble")


def monthly_mean_climatology(self):
    """
    Calculate the monthly mean climatologies
    Defined as the minimum value in each month across all years.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_mean_climatology is deprecated. Use tmean!")
    ymonstat(self, stat="mean")


def monthly_min_climatology(self):
    """
    Calculate the monthly minimum climatologies
    Defined as the minimum value in each month across all years.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_min_climatology is deprecated. Use tmin!")
    ymonstat(self, stat="min")


def monthly_max_climatology(self):
    """
    Calculate the monthly maximum climatologies
    Defined as the maximum value in each month across all years.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_max_climatology is deprecated. Use tmax!")
    ymonstat(self, stat="max")


def monthly_range_climatology(self):
    """
    Calculate the monthly range climatologies
    Defined as the range of value in each month across all years.
    This applies to each file in an ensemble.
    """
    warnings.warn(message="Warning: monthly_range_climatology is deprecated. Use trange!")
    ymonstat(self, stat="range")
def yearlystat(self, stat="mean"):
    """Function to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -year{stat}"

    run_this(cdo_command, self, output="ensemble")


def annual_mean(self):
    """
    Calculate the annual mean for each variable
    """
    warnings.warn(message="Warning: annual_mean is deprecated. Use tmean!")
    yearlystat(self, stat="mean")


def annual_min(self):
    """
    Calculate the annual minimum for each variable
    """
    warnings.warn(message="Warning: annual_min is deprecated. Use tmin!")
    yearlystat(self, stat="min")


def annual_max(self):
    """
    Calculate the annual maximum for each variable
    """
    warnings.warn(message="Warning: annual_max is deprecated. Use tmax!")
    yearlystat(self, stat="max")


def annual_range(self):
    """
    Calculate the annual range for each variable
    """
    warnings.warn(message="Warning: annual_range is deprecated. Use trange!")
    yearlystat(self, stat="range")


def annual_sum(self):
    """
    Calculate the annual sum for each variable
    """
    warnings.warn(message="Warning: annual_sum is deprecated. Use tsum!")
    yearlystat(self, stat="sum")

def seasstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -seas{stat}"

    run_this(cdo_command, self, output="ensemble")


def seasonal_mean(self):
    """
    Calculate the seasonal mean for each year. Applies at the grid cell level.
    """
    warnings.warn(message="Warning: seasonal_mean is deprecated. Use tmean!")
    seasstat(self, stat="mean")


def seasonal_min(self):
    """
    Calculate the seasonal minimum for each year. Applies at the grid cell level.
    """
    warnings.warn(message="Warning: seasonal_min is deprecated. Use tmin!")
    seasstat(self, stat="min")


def seasonal_max(self):
    """
    Calculate the seasonal maximum for each year. Applies at the grid cell level.
    """
    warnings.warn(message="Warning: seasonal_max is deprecated. Use tmax!")
    seasstat(self, stat="max")


def seasonal_range(self):
    """
    Calculate the seasonal range for each year. Applies at the grid cell level.
    """
    warnings.warn(message="Warning: seasonal_range is deprecated. Use trange!")
    seasstat(self, stat="range")

def seasclim(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""
    # create cdo call and run it
    cdo_command = f"cdo -yseas{stat}"

    run_this(cdo_command, self, output="ensemble")


def seasonal_mean_climatology(self):
    """
    Calculate a climatological seasonal mean

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    """
    warnings.warn(message="Warning: seasonal_mean_climatology is deprecated. Use tmean!")

    seasclim(self, stat="mean")


def seasonal_min_climatology(self):
    """
    Calculate a climatological seasonal min
    This is defined as the minimum value in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    warnings.warn(message="Warning: seasonal_min_climatology is deprecated. Use tmin!")
    seasclim(self, stat="min")


def seasonal_max_climatology(self):
    """
    Calculate a climatological seasonal max
    This is defined as the maximum value in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    warnings.warn(message="Warning: seasonal_max_climatology is deprecated. Use tmax!")
    seasclim(self, stat="max")


def seasonal_range_climatology(self):
    """
    Calculate a climatological seasonal range
    This is defined as the range of values in each season across all years.

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum

    """
    warnings.warn(message="Warning: seasonal_range_climatology is deprecated. Use trange!")
    seasclim(self, stat="range")

#####################################################
# Delete these in April 2021
#####################################################

def cell_areas(self, join=True):
    """
    Calculate the area of grid cells.
    Area of grid cells is given in square meters.

    Parameters
    -------------
    join: boolean
        Set to False if you only want the cell areas to be in the output.
        join=True adds the areas as a variable to the dataset. Defaults to True.
    """

    if isinstance(join, bool) is False:
        raise TypeError("join is not boolean")

    # release if you need to join the cell areas to the original file
    if join:
        self.run()

    # get the cdo version
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]

    # first run the join case
    if join:

        new_files = []
        new_commands = []

        for ff in self:

            if cdo_version in ["1.9.3", "1.9.4", "1.9.5", "1.9.6"]:

                # in cdo < 1.9.6 chaining doesn't work with merge

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target1 = temp_file(".nc")

                cdo_command = f"cdo -gridarea {ff} {target1}"
                cdo_command = tidy_command(cdo_command)
                target1 = run_cdo(cdo_command, target1)
                new_files.append(target1)
                new_commands.append(cdo_command)

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} {target1} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

            else:

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} -gridarea {ff} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

        for x in new_commands:
            self.history.append(x)

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)

        self._hold_history = copy.deepcopy(self.history)

        cleanup()

    else:

        cdo_command = "cdo -gridarea"
        run_this(cdo_command, self, output="ensemble")

    # add units

    self.set_units({"cell_area": "m^2"})

    if join:
        self.run()
        self.disk_clean()




def remove_variables(self, vars=None):
    """
    Remove variables
    This will remove stated variables from files in the dataset.

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the dataset.
        Variables that are listed but not in the dataset will be ignored
    """
    warnings.warn(message="Warning: remove_variables is deprecated. Use drop!")

    # Some checks on the validity of variables supplied
    if vars is None:
        raise ValueError("Please supplied vars")

    if type(vars) is not list:
        vars = [vars]

    for vv in vars:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

    vars = str_flatten(vars, ",")

    # create the cdo command and run it
    cdo_command = f"cdo -delete,name={vars}"
    run_this(cdo_command, self, output="ensemble")
