import warnings
from datetime import datetime, timedelta
import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.session import nc_safe, session_info, append_safe, remove_safe
from nctoolkit.temp_file import temp_file
from nctoolkit.runthis import run_this
from nctoolkit.show import nc_years, nc_times
from nctoolkit.crop import crop


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

    if type(period) is not list:
        raise TypeError("Invalid range supplied")

    if len(period) != 2:
        raise ValueError("range must be a 2 variable list!")

    if type(period[0]) is str and type(period[1]) is str:
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

    if type(season) is not str:
        raise TypeError("Invalid season supplied")

    if season not in ["DJF", "MAM", "JJA", "SON"]:
        raise ValueError("Invalid season supplied")

    cdo_command = f"cdo -select,season={season}"
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
    if type(months) is range:
        months = list(months)

    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints,
    # just in case floats have been provided

    for x in months:
        if type(x) is not int:
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

    if type(years) is range:
        years = list(years)

    if type(years) is not list:
        years = [years]

    # convert years to int

    for yy in years:
        if type(yy) is not int:
            raise TypeError(f"{yy} is not an int")

    if self._merged is False:

        missing_files = 0

        n_removed = 0

        # loop through all of the files and remove any that do not have valid years
        new_current = []

        for ff in self:

            all_years = nc_years(ff)
            all_years = list(set(all_years))
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
            raise ValueError("Data for none of the years is available!")

        if n_removed > 0:
            warnings.warn(
                message="A total of "
                + str(n_removed)
                + " files did not have valid years, so were removed from the dataset!"
            )

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

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    for vv in vars_list:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

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


def select(self, **kwargs):
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
    months : list, range or int
        Month(s) to select.
    years : list,range or int
        Years(s) to select. These should be integers
    range : list
        List of the form [date_min, date_max], where dates must be datetime objects or strings of the form "DD/MM/YYYY" or "DD-MM-YYYY".
        Times selected will be on or after date_min and before date_max.

    timesteps : list or int
        time step(s) to select. For example, if you wanted the first time step
        set times=0.

    Examples
    ------------
    If you want to select a single variable do the following:

        >>> ds.select(variable = "var")

    If you want to select a list of variables, do this:

        >>> ds.select(variable = ["var1", "var2"])

    If you want to select data for January, do the following:

        >>> ds.select(month = 1)

    If you want to select a range of months, do the following:

        >>> ds.select(months = range(1, 7))

    If you want to select a range of years, for example the 2010s, do the following:

        >>> ds.select(years = range(2010, 2020))

    If you want to select the first two timesteps in a dataset, do the following:

        >>> ds.select(timesteps = [0,1])


    """

    non_selected = True

    for key in kwargs:

        if "ran" in key and non_selected:
            select_period(self, kwargs[key])
            non_selected = False

        if "var" in key and non_selected:
            select_variables(self, kwargs[key])
            non_selected = False

        if "mon" in key and non_selected:
            select_months(self, kwargs[key])
            non_selected = False

        if "year" in key and non_selected:
            select_years(self, kwargs[key])
            non_selected = False

        if "seas" in key and non_selected:
            select_seasons(self, kwargs[key])
            non_selected = False

        if "time" in key and non_selected:
            select_timesteps(self, kwargs[key])
            non_selected = False

    if non_selected:
        raise AttributeError(f"{key} is not a valid select method")
