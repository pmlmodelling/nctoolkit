
import copy
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_nco, tidy_command
from nctoolkit.temp_file import temp_file
from nctoolkit.session import nc_safe
from nctoolkit.time_stat import *
from nctoolkit.verticals import *
import warnings





def clip(self, lon=[-180, 180], lat=[-90, 90], nco=False):
    """
    Crop to a rectangular longitude and latitude box

    Parameters
    -------------
    lon: list
        The longitude range to select. This must be two variables,
        between -180 and 180 when nco = False.
    lat: list
        The latitude range to select. This must be two variables,
        between -90 and 90 when nco = False.
    nco: boolean
        Do you want this to use NCO for clipping? Defaults to False,
        and uses CDO. Set to True if you want to call NCO.
        NCO is typically better at handling very large horizontal grids.
    """
    warnings.warn(message="Warning: clip is deprecated. Use crop!")

    # check validity of lon/lat supplied
    if (type(lon) is not list) or (type(lat) is not list):
        raise TypeError("Check that lon/lat ranges are tuples")

    if len(lon) != 2:
        raise ValueError("lon is a list of more than 2 variables")

    if len(lat) != 2:
        raise ValueError("lat is a list of more than 2 variables")

    for ll in lon:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lon is not a float or int")

    for ll in lat:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lat is not a float or int")

    # now, clip to the lonlat box we need

    if lat[1] < lat[0]:
        raise ValueError("Check lat order")
    if lon[1] < lon[0]:
        raise ValueError("Check lon order")

    if nco is False:
        if (lon[0] >= -180) and (lon[1] <= 180) and (lat[0] >= -90) and (lat[1] <= 90):
            lat_box = str_flatten(lon + lat)
            cdo_command = "cdo -sellonlatbox," + lat_box
            cdo_command = tidy_command(cdo_command)

            run_this(cdo_command, self, output="ensemble")
            return None
        else:
            raise ValueError("The lonlat box supplied is not valid!")

    self.run()

    new_files = []
    new_commands = []

    for ff in self:

        # find the names of lonlat

        out = subprocess.run(
            f"cdo griddes {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        lon_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x
        ][0].split(" ")[-1]
        lat_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x
        ][0].split(" ")[-1]
        target = temp_file("nc")

        nco_command = (
            "ncea -d "
            + lat_name
            + ","
            + str(float(lat[0]))
            + ","
            + str(float(lat[1]))
            + " -d "
            + lon_name
            + ","
            + str(float(lon[0]))
            + ","
            + str(float(lon[1]))
            + " "
            + ff
            + " "
            + target
        )
        if lon == [-180, 180]:
            nco_command = (
                "ncea -d "
                + lat_name
                + ","
                + str(float(lat[0]))
                + ","
                + str(float(lat[1]))
                + " "
                + ff
                + " "
                + target
            )

        if lat == [-90, 90]:
            nco_command = (
                "ncea  -d "
                + lon_name
                + ","
                + str(float(lon[0]))
                + ","
                + str(float(lon[1]))
                + " "
                + ff
                + " "
                + target
            )

        target = run_nco(nco_command, target)

        new_commands.append(nco_command)

        new_files.append(target)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()
    self.disk_clean()


# deprecate this in December 2020

def release(self):
    """
    Run all stored commands in a dataset
    """
    warnings.warn(message="Warning: release is deprecated. Use run!")

    # the first step is to set the run status to true

    if (self._execute is False) and (len(self.history) > len(self._hold_history)):
        self._execute = True

        cdo_command = "cdo "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self, output=output_method)

        self._merged = False

        self._execute = False
        self._zip = False

        if len(self._safe) > 0:
            for ff in self._safe:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        self._safe = []

        cleanup()

        self._thredds = False




# deprecate this in January 2021
def select_timestep(self, times=None):
    """
    Select timesteps from a dataset

    Parameters
    -------------
    times : list or int
        time step(s) to select. For example, if you wanted the first time step
        set times=0.
    """
    warnings.warn(message="select_timestep is deprecated. Use select_seasons")

    if times is None:
        raise ValueError("Please supply times")

    if type(times) is range:
        times = list(times)

    if type(times) is not list:
        times = [times]

    for tt in times:
        if type(tt) is not int:
            raise TypeError(f"{tt} is not an int")
        if tt < 0:
            raise ValueError(f"{tt} is not a valid timestep")

    # all of the variables in months need to be converted to ints,
    # just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = f"cdo -seltimestep,{times}"

    run_this(cdo_command, self, output="ensemble")

# deprecate this in January 2021

def select_season(self, season=None):
    """
    Select season from a dataset

    Parameters
    -------------
    season : str
        Season to select. One of "DJF", "MAM", "JJA", "SON".
    """

    warnings.warn(message="select_season is deprecated. Use select_seasons")

    if season is None:
        raise ValueError("No season supplied")

    if type(season) is not str:
        raise TypeError("Invalid season supplied")

    if season not in ["DJF", "MAM", "JJA", "SON"]:
        raise ValueError("Invalid season supplied")

    cdo_command = f"cdo -select,season={season}"
    run_this(cdo_command, self, output="ensemble")

def write_nc(self, out, zip=True, overwrite=False):
    """
    Save a dataset to a named file
    This will only work with single file datasets.

    Parameters
    -------------
    out : str
        Output file name.
    zip : boolean
        True/False depending on whether you want to zip the file. Default is True.
    overwrite : boolean
        If out file exists, do you want to overwrite it? Default is False.
    """

    warnings.warn(message = "write_nc has been deprecated. Please use to_nc")

    # If the output file exists, cdo cannot simultaneously have it opened and written to
    if (os.path.exists(out)) and (overwrite is True):
        self.run()

    if type(self.current) is list:
        ff = copy.deepcopy(self.current)
    else:
        ff = [copy.deepcopy(self.current)]

    # Figure out if it is possible to write the file, i.e. if a dataset is still an
    # ensemble, you cannot write.
    write = False

    if type(self.current) is str:
        write = True

    if self._merged:
        write = True

    if write is False:
        raise ValueError("You cannot save multiple files!")

    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error
    if (os.path.exists(out)) and (overwrite is False):
        raise ValueError("The out file exists and overwrite is set to false")

    if len(self.history) == len(self._hold_history):
        if zip:
            cdo_command = f"cdo -z zip_9 copy {ff[0]} {out}"
            run_cdo(cdo_command, target=out, overwrite=overwrite)

            self.history.append(cdo_command)

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

    if type(self.current) is str:
        os.system("ncview " + self.current + "&")
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
