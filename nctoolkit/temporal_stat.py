import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.temporals import *
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe
import warnings


def time_stat(self, stat="mean", over="time"):
    """Method to calculate a stat over all time steps"""
    # create cdo command and run it

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    if over == "time":
        cdo_command = f"cdo -tim{stat}"
        run_this(cdo_command, self, output="ensemble")
        return None

    if stat not in ["mean", "sum", "min", "max", "range", "var", "cumsum", "std"]:
        raise ValueError(f"{stat} is not a valid CDO stat!")

    # some tidying of over
    if isinstance(over, str):
        over = [over]

    over = [x.lower() for x in over]
    over = ["month" if "mon" in x else x for x in over]
    over = ["year" if "yea" in x else x for x in over]
    over = ["season" if "sea" in x else x for x in over]

    for x in over:
        if x not in ["day", "month", "year", "season", "hour"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping over season and day and month makes no sense

    if "season" in over and ("month" in over or "day" in over):
        raise ValueError("You cannot group over season and day or month")

    over = sorted(list(set(over)))

    if over == ["day", "month"]:
        over = ["day"]

    if over == ["day", "hour", "month"]:
        over = ["day", "hour"]

    if over == ["day", "hour", "month", "year"]:
        over = ["day", "hour", "year"]
    # sort over alphabetically

    run = False

    # single variables
    # daily climatology
    if over == ["day"]:
        run = True
        ydaystat(self, stat=stat)
        return None

    if over == ["day", "hour"]:
        run = True
        yhourstat(self, stat=stat)
        return None

    if over == ["day", "hour",  "year"]:
        run = True
        hourstat(self, stat=stat)
        return None

    if over == ["hour"]:
        run = True
        dhourstat(self, stat=stat)
        return None

    # monthly climatology
    if over == ["month"]:
        run = True
        ymonstat(self, stat=stat)
        return None

    # annual mean
    if over == ["year"]:
        run = True
        yearlystat(self, stat=stat)
        return None

    # seasonal climatology
    if over == ["season"]:
        run = True
        seasclim(self, stat=stat)
        return None

    # seasonal climatology
    if over == ["season", "year"]:
        run = True
        seasstat(self, stat=stat)
        return None

    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        run = True
        dailystat(self, stat=stat)
        return None

    # monthly mean

    if over == ["month", "year"]:
        run = True
        monstat(self, stat=stat)
        return None
    if run is False:
        raise ValueError(f"Grouping {over} is currently not supported!")



def tsum(self, over="time", align = "right"):
    """
    Calculate the temporal sum of all variables

    Parameters
    -------------
    align = str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    """
    self.align(align)
    time_stat(self, stat="sum", over=over)


def na_count(self, over="time", align = "right"):
    """
    Calculate the number of missing values

    Parameters
    -------------
    over: str or list
        Time periods to to the count over over. Options are 'time', 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    """
    self.align(align)

    self.run()

    for vv in self.variables:
        self.cdo_command(f"-aexpr,'{vv}=isMissval({vv})'")

    self.tsum(over=over)


def na_frac(self, over="time", align = "right"):
    """
    Calculate the number of missing values

    Parameters
    -------------
    over: str or list
        Time periods to to the count over over. Options are 'time', 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    """
    self.align(align)

    self.run()

    for vv in self.variables:
        self.cdo_command(f"-aexpr,'{vv}=isMissval({vv})'")

    self.tmean(over=over)


def tmean(self, over="time", align = "right"):
    """
    Calculate the temporal mean of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate mean over all time steps. Do the following:

        >>> ds.tmean()

    If you want to calculate the mean for each year in a dataset, do this:

        >>> ds.tmean("year")

    If you want to calculate the mean for each month in a dataset, do this:

        >>> ds.tmean("month")

    If you want to calculate the mean for each month in each year in a dataset, do this:

        >>> ds.tmean(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological mean, you would do this:

        >>> ds.tmean( "month")

    A daily climatological mean would be the following:

        >>> ds.tmean( "day")


    """
    self.align(align = align)
    time_stat(self, stat="mean", over=over)


def tmin(self, over="time", align = "right"):
    """
    Calculate the temporal minimum of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.

    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate minimum over all time steps. Do the following:

        >>> ds.tmin()

    If you want to calculate the minimum for each year in a dataset, do this:

        >>> ds.tmin("year")

    If you want to calculate the minimum for each month in a dataset, do this:

        >>> ds.tmin("month")

    If you want to calculate the minimum for each month in each year in a dataset, do this:

        >>> ds.tmin(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological min, you would do this:

        >>> ds.tmin( "month")

    A daily climatological minimum would be the following:

        >>> ds.tmin( "day")

    """
    self.align(align = align)
    time_stat(self, stat="min", over=over)


def tmax(self, over="time", align = "right"):
    """
    Calculate the temporal maximum of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
    align = str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate maximum over all time steps. Do the following:

        >>> ds.tmax()

    If you want to calculate the maximum for each year in a dataset, do this:

        >>> ds.tmax("year")

    If you want to calculate the maximum for each month in a dataset, do this:

        >>> ds.tmax("month")

    If you want to calculate the maximum for each month in each year in a dataset, do this:

        >>> ds.tmax(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological max, you would do this:

        >>> ds.tmax( "month")

    A daily climatological maximum would be the following:

        >>> ds.tmax( "day")
    """
    self.align(align = align)
    time_stat(self, stat="max", over=over)


def tmedian(self, over="time", align = "right"):
    """
    Calculate the temporal median of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate median over all time steps. Do the following:

        >>> ds.tmedian()

    If you want to calculate the median for each year in a dataset, do this:

        >>> ds.tmedian("year")

    If you want to calculate the median for each month in a dataset, do this:

        >>> ds.tmedian("month")

    If you want to calculate the median for each month in each year in a dataset, do this:

        >>> ds.tmedian(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological median, you would do this:

        >>> ds.tmedian( "month")

    A daily climatological median would be the following:

        >>> ds.tmedian( "day")
    """
    self.align(align = align)
    self.tpercentile(p=50, over=over)


def trange(self, over="time", align = "right"):
    """
    Calculate the temporal range of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate range over all time steps. Do the following:

        >>> ds.trange()

    If you want to calculate the range for each year in a dataset, do this:

        >>> ds.trange("year")

    If you want to calculate the range for each month in a dataset, do this:

        >>> ds.trange("month")

    If you want to calculate the range for each month in each year in a dataset, do this:

        >>> ds.trange(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological range, you would do this:

        >>> ds.trange( "month")

    A daily climatological range would be the following:

        >>> ds.trange( "day")

    """
    self.align(align = align)
    time_stat(self, stat="range", over=over)


def tvar(self, over="time", align = "right"):
    """
    Calculate the temporal variance of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"


    Examples
    ------------
    If you want to calculate variance over all time steps. Do the following:

        >>> ds.tvar()

    If you want to calculate the variance for each year in a dataset, do this:

        >>> ds.tvar("year")

    If you want to calculate the variance for each month in a dataset, do this:

        >>> ds.tvar("month")

    If you want to calculate the variance for each month in each year in a dataset, do this:

        >>> ds.tvar(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological var, you would do this:

        >>> ds.tvar( "month")

    A daily climatological variance would be the following:

        >>> ds.tvar( "day")
    """
    self.align(align = align)
    time_stat(self, stat="var", over=over)


def tstdev(self, over="time", align = "right"):
    """
    Calculate the temporal standard deviation of all variables

    Parameters
    -------------
    over: str or list
        Time periods to average over. Options are 'year', 'month', 'day'.
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"


    Examples
    ------------
    If you want to calculate standard deviation over all time steps. Do the following:

        >>> ds.tstdev()

    If you want to calculate the standard deviation for each year in a dataset, do this:

        >>> ds.tstdev("year")

    If you want to calculate the standard deviation for each month in a dataset, do this:

        >>> ds.tstdev("month")

    If you want to calculate the standard deviation for each month in each year in a dataset, do this:

        >>> ds.tstdev(["year", "month"])

    This method will also let you easily calculate climatologies. So, if you wanted to calculate
    a monthly climatological var, you would do this:

        >>> ds.tstdev("month")

    A daily climatological standard deviation would be the following:

        >>> ds.tstdev("day")
    """
    self.align(align = align)
    time_stat(self, stat="std", over=over)


def tcumsum(self, align = "right"):
    """
    Calculate the temporal cumulative sum of all variables

    Parameters
    -------------
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate the cumulative sum for all variables over all timesteps, do this:

        >>> ds.tcumsum()

    """
    self.align(align=align)
    # create cdo command and runit
    time_stat(self, stat="cumsum")


def tpercentile(self, p=None, over="time", align = "right"):
    """
    Calculate the temporal percentile of all variables

    Parameters
    -------------
    p: float or int
        Percentile to calculate
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------
    If you want to calculate the 20th percentile over all time steps. Do the following:

        >>> ds.tpercentile(20)

    If you want to calculate the 20th percentile for each year in a dataset, do this:

        >>> ds.tpercentile(20)

    """
    self.align(align=align)

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    over = over
    if p is None:
        raise ValueError("Please supply p")

    if not isinstance(p, (int, float)):
        raise TypeError("p is a " + str(type(p)) + ", not int or float")

    if (p < 0) or (p > 100):
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    self.run()

    # create cdo command and run it

    if isinstance(over, str):
        over = [over]

    for x in over:
        if x not in ["day", "month", "year", "season", "time"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping over season and day and month makes no sense

    if "season" in over and ("month" in over or "day" in over):
        raise ValueError("You cannot group over season and day or month")

    over = sorted(list(set(over)))

    if over == ["day", "month"]:
        over = ["day"]

    if over == ["time"]:
        perc_term = "cdo -timpctl,"
        min_command = " -timmin "
        max_command = " -timmax "

    # single variables
    # daily climatology
    if over == ["day"]:
        perc_term = "cdo -ydaypctl,"
        min_command = " -ydaymin "
        max_command = " -ydaymax "

    # monthly climatology
    if over == ["month"]:
        perc_term = "cdo -ymonpctl,"
        min_command = " -ymonmin "
        max_command = " -ymonmax "

    # annual mean
    if over == ["year"]:
        perc_term = "cdo -yearpctl,"
        min_command = " -yearmin "
        max_command = " -yearmax "

    # seasonal climatology
    if over == ["season"]:
        perc_term = "cdo -yseaspctl,"
        min_command = " -yseasmin "
        max_command = " -yseasmax "

    # seasonal climatology
    if over == ["season", "year"]:
        perc_term = "cdo -seaspctl,"
        min_command = " -seasmin "
        max_command = " -seasmax "

    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        perc_term = "cdo -daypctl,"
        min_command = " -daymin "
        max_command = " -daymax "

    # monthly mean

    if over == ["month", "year"]:
        perc_term = "cdo -monpctl,"
        min_command = " -monmin "
        max_command = " -monmax "

    new_files = []
    new_commands = []
    for ff in self:
        target = temp_file("nc")

        cdo_command = (
                perc_term
            #"cdo -timpctl,"
            + str(p)
            + " "
            + ff
            + min_command
            + ff
            + max_command
            + ff
            + " "
            + target
        )

        cdo_command = tidy_command(cdo_command)
        target = run_cdo(cdo_command, target, precision=self._precision)
        new_files.append(target)
        new_commands.append(cdo_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()
