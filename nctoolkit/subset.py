import warnings
import numpy as np
from datetime import datetime, timedelta

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this
from nctoolkit.show import nc_years
from nctoolkit.utils import cdo_version, version_above, name_check



def to_date(x):
    if "-" in x:
        new = x.split("-")
    if "/" in x:
        new = x.split("/")
    if len(new) != 3:
        raise ValueError(f"{x} could not be parsed")
    day = int(new[0])
    month = int(new[1])
    year = int(new[2])
    return datetime(year, month, day)

def select_levels(self, levels=None):
    """
    Select season from a dataset

    Parameters
    -------------
    levels : list
        List of the form [min_level, max_level]. Levels/depth between the two will be selected
    """
    if not isinstance(levels, list):
        type(levels)
        try:
            levels = float(levels)
        except:
            raise ValueError("levels provided are not valid!")

    if isinstance(levels, list):
        try:
            levels[0] = int(np.floor(float(levels[0])))
            levels[1] = int(np.ceil(float(levels[1])))
        except:
            raise ValueError("levels provided are not valid!")
        if levels[0] > levels[1]:
            raise ValueError("levels have the wrong order")
        levels = f"{levels[0]}/{levels[1]}" 

    cdo_command =  f"cdo -sellevel,{levels}"
        
    run_this(cdo_command, self, "ensemble")


def select_period(self, period=None):
    """
    Select season from a dataset

    Parameters
    -------------
    period : list
        List of the form [date_min, date_max], where dates must be datetime objects or strings of the form "DD/MM/YYYY" or "DD-MM-YYYY".
    """

    if period is None:
        raise ValueError("No range supplied")

    if not isinstance(period, list):
        raise TypeError("Invalid range supplied")

    if len(period) != 2:
        raise ValueError("range must be a 2 variable list!")

    if isinstance(period[0], str) and isinstance(period[1], str):
        period = [to_date(x) for x in period]

    for x in period:
        if isinstance(x, datetime) is False:
            raise ValueError("Please provide datetime objects in range")

    if period[0] >= period[1]:
        raise ValueError("Range order is incorrect")

    start = str(period[0]).split(" ")[0]
    end = period[1] - timedelta(days=1)
    end = str(end).split(" ")[0]
    cdo_command = f"cdo -seldate,{start},{end}"

    run_this(cdo_command, self, "ensemble")


def select_seasons(self, season=None):
    """
    Select season from a dataset

    Parameters
    -------------
    season : str
        Season to select. One of "DJF", "MAM", "JJA", "SON".
    """

    if season is None:
        raise ValueError("No season supplied")

    if not isinstance(season, str):
        raise TypeError("Invalid season supplied")

    if season not in ["DJF", "MAM", "JJA", "SON"]:
        raise ValueError("Invalid season supplied")

    cdo_command = f"cdo -select,season={season}"
    run_this(cdo_command, self, output="ensemble")

def select_hours(self, hours=None):
    """
    Select hours from a dataset
    This method will subset the dataset to only contain hours within the list given.
    A warning message will be provided when there are missing hours.

    Parameters
    -------------
    hours : list, range or int
        Month(s) to select.
    """

    if hours is None:
        raise ValueError("Please supply hours")

    # check validity of hours
    if isinstance(hours, range):
        hours = list(hours)

    if not isinstance(hours, list):
        hours = [hours]
    # all of the variables in hours need to be converted to ints,
    # just in case floats have been provided
    # coerce to int if numpy float etc.

    hours = [int(x) if "int" in str(type(x)) else x for x in hours]


    for x in hours:
        if not isinstance(x, int):
            raise TypeError(f"{x} is not an int")
        if x not in list(range(1, 32)):
            raise ValueError(f"{x} is not a hour")

    hours = str_flatten(hours, ",")

    cdo_command = f"cdo -selhour,{hours}"
    run_this(cdo_command, self, output="ensemble")


def select_days(self, days=None):
    """
    Select days from a dataset
    This method will subset the dataset to only contain days within the list given.
    A warning message will be provided when there are missing days.

    Parameters
    -------------
    days : list, range or int
        Month(s) to select.
    """

    if days is None:
        raise ValueError("Please supply days")

    # check validity of days
    if isinstance(days, range):
        days = list(days)

    if not isinstance(days, list):
        days = [days]
    # all of the variables in days need to be converted to ints,
    # just in case floats have been provided
    # coerce to int if numpy float etc.

    days = [int(x) if "int" in str(type(x)) else x for x in days]


    for x in days:
        if not isinstance(x, int):
            raise TypeError(f"{x} is not an int")
        if x not in list(range(1, 32)):
            raise ValueError(f"{x} is not a day")

    days = str_flatten(days, ",")

    cdo_command = f"cdo -selday,{days}"
    run_this(cdo_command, self, output="ensemble")


def select_months(self, months=None):
    """
    Select months from a dataset
    This method will subset the dataset to only contain months within the list given.
    A warning message will be provided when there are missing months.

    Parameters
    -------------
    months : list, range or int
        Month(s) to select.
    """

    if months is None:
        raise ValueError("Please supply months")

    # check validity of months
    if isinstance(months, range):
        months = list(months)

    if not isinstance(months, list):
        months = [months]
    # all of the variables in months need to be converted to ints,
    # just in case floats have been provided
    # coerce to int if numpy float etc.

    months = [int(x) if "int" in str(type(x)) else x for x in months]


    for x in months:
        if not isinstance(x, int):
            raise TypeError(f"{x} is not an int")
        if x not in list(range(1, 13)):
            raise ValueError(f"{x} is not a month")

    months = str_flatten(months, ",")

    cdo_command = f"cdo -selmonth,{months}"
    run_this(cdo_command, self, output="ensemble")


def select_years(self, years=None):
    """
    Select years from a dataset
    This method will subset the dataset to only contain years within the list given.
    A warning message will be provided when there are missing years.

    Parameters
    -------------
    years : list,range or int
        Years(s) to select. These should be integers

    """
    if years is None:
        raise ValueError("Please supply years")

    if isinstance(years, range):
        years = list(years)

    if not isinstance(years, list):
        years = [years]

    # convert years to int
    years = [int(x) if "int" in str(type(x)) else x for x in years]

    for yy in years:
        if not isinstance(yy, int):
            raise TypeError(f"{yy} is not an int")

    if self._merged is False:

        missing_files = 0

        n_removed = 0

        # loop through all of the files and remove any that do not have valid years
        new_current = []


        all_check = []

        for ff in self:

            all_years = nc_years(ff)
            all_years = list(set(all_years))
            all_check+=all_years
            all_years = [int(v) for v in all_years]
            inter = [element for element in all_years if element in years]

            if len(inter) > 0:
                new_current.append(ff)
            if len(inter) == 0:
                n_removed += 1

            # figure out if any of the files actually have years
            # outide the period required
            if len(inter) > 0:
                if len([yy for yy in all_years if yy not in years]) > 0:
                    missing_files += 1

        if len(new_current) == 0:
            raise ValueError("Data is not available for the years selected!")

        if n_removed > 0:
            warnings.warn(
                message="A total of "
                + str(n_removed)
                + " files did not have valid years, so were removed from the dataset!"
            )

        missing_years = [str(x) for x in years if x not in all_years]
        if len(missing_years) > 0:
            len_missing = len(missing_years)
            missing_years = [int(x) for x in missing_years]
            if set(range(min(missing_years), max(missing_years) + 1)) == set(missing_years):
                if len(missing_years) > 1:
                    missing_years = str(min(missing_years)) + "-" + str(max(missing_years))
                else:
                    missing_years = str(missing_years[0])
            else:
                missing_years = [str(x) for x in missing_years]
                missing_years = str_flatten(missing_years, ",")
            if missing_files == 0:
                if len_missing == 1:
                    warnings.warn(f"The following year was not available in the dataset: {missing_years}")
                else:
                    warnings.warn(f"{len_missing} years were not available in the dataset: {missing_years}")

        self.current = new_current

        if missing_files > 0:
            years = str_flatten(years, ",")

            cdo_command = f"cdo -selyear,{years}"

            run_this(cdo_command, self, output="ensemble")
    else:
        years = str_flatten(years, ",")

        cdo_command = f"cdo -selyear,{years}"

        run_this(cdo_command, self, output="one")

    cleanup()


def select_variables(self, vars=None):
    """
    Select variables from a dataset

    Parameters
    -------------
    vars : list or str
        Variable(s) to select.
    """

    if vars is None:
        raise ValueError("vars was not supplied")

    if isinstance(vars, str):
        vars_list = [vars]
    else:
        vars_list = vars

    for vv in vars_list:
        if not isinstance(vv, str):
            raise TypeError(f"{vv} is not a str")

    for x in vars_list:
        if name_check(x) is False:
            if ("*" not in x) and ("?" not in x):
                raise ValueError(f"{x} is not a valid netCDF variable name")

    vars_list = str_flatten(vars_list, ",")

    cdo_command = f"cdo -selname,{vars_list}"

    run_this(cdo_command, self, output="ensemble")


def select_timesteps(self, times=None):
    """
    Select timesteps from a dataset

    Parameters
    -------------
    times : list or int
        time step(s) to select. For example, if you wanted the first time step
        set times=0.
    """

    if times is None:
        raise ValueError("Please supply times")

    if isinstance(times, range):
        times = list(times)

    if not isinstance(times, list):
        times = [times]

    for tt in times:
        if not isinstance(tt, int):
            raise TypeError(f"{tt} is not an int")
        if tt < 0:
            if version_above(cdo_version(), "2.0.0") is False:
                raise ValueError(f"Please install CDO version 2.0.5 or above for negative timestep selections")

    # all of the variables in months need to be converted to ints,
    # just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = f"cdo -seltimestep,{times}"

    run_this(cdo_command, self, output="ensemble")


def subset(self, **kwargs):
    """
    A method for subsetting datasets to specific variables, years, longitudes etc.
    Operations are applied in the order supplied.

    Parameters
    -------------
    *kwargs
        Possible arguments: variables, years, months, seasons, timesteps, lon, lat

        Note: this uses partial matches. So year, month, var etc. will also work


    Each kwarg works as follows:

    variables : str or list
        A variable or list of variables to select. This method will accept wild cards.
        So using 'var*' would select all variables beginning with 'var'.
    seasons : str
        Seasons to select. One of "DJF", "MAM", "JJA", "SON".
    days : list, range or int
        Days(s) to select.
    months : list, range or int
        Month(s) to select.
    years : list,range or int
        Years(s) to select. These should be integers
    hours : list, range or int
        Hours(s) to select.
    range : list
        List of the form [date_min, date_max], where dates must be datetime objects or strings of the form "DD/MM/YYYY" or "DD-MM-YYYY".
        Times selected will be on or after date_min and before date_max.

    timesteps : list or int
        time step(s) to select. For example, if you wanted the first time step
        set times=0.

    lon: list
        The longitude range to select. This must be two variables,
        between -180 and 180.
    lat: list
        The latitude range to select. This must be two variables,
        between -90 and 90.

    levels : list
        List of the form [min_level, max_level]. Levels/depths between the two will be selected

    Examples
    ------------
    If you want to select a single variable do the following:

        >>> ds.subset(variable = "var")

    If you want to select a list of variables, do this:

        >>> ds.subset(variable = ["var1", "var2"])

    If you want to select data for January, do the following:

        >>> ds.subset(month = 1)

    If you want to select a range of months, do the following:

        >>> ds.subset(months = range(1, 7))

    If you want to select a range of years, for example the 2010s, do the following:

        >>> ds.subset(years = range(2010, 2020))

    If you want to select the first two timesteps in a dataset, do the following:

        >>> ds.subset(timesteps = [0,1])


    """

    non_selected = True

    lon = None
    lat = None
    for key in kwargs:
        if "lon" in key.lower():
            lon = kwargs[key]
        if "lat" in key.lower():
            lat = kwargs[key]
    if lon is not None or lat is not None:
        self.crop(lon = lon, lat = lat)
        non_selected = False

    for key in kwargs:

        if "ran" in key.lower():
            select_period(self, kwargs[key])
            non_selected = False

        if "var" in key.lower():
            select_variables(self, kwargs[key])
            non_selected = False

        if "mon" in key.lower():
            select_months(self, kwargs[key])
            non_selected = False

        if "year" in key.lower():
            select_years(self, kwargs[key])
            non_selected = False

        if "seas" in key.lower():
            select_seasons(self, kwargs[key])
            non_selected = False

        if "time" in key.lower():
            select_timesteps(self, kwargs[key])
            non_selected = False

        if "day" in key.lower():
            select_days(self, kwargs[key])
            non_selected = False

        if "hour" in key.lower():
            select_hours(self, kwargs[key])
            non_selected = False

        if "lev" in key.lower() or "depth" in key.lower():
            select_levels(self, kwargs[key])
            non_selected = False


    if non_selected:
        raise AttributeError(f"{key} is not a valid select method")
