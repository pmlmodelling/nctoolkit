import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.temporals import *
from nctoolkit.temp_file import temp_file
import warnings


def time_stat(self, stat="mean", over = "time"):
    """Method to calculate a stat over all time steps"""
    # create cdo command and run it
    if over == "time":
        cdo_command = f"cdo -tim{stat}"
        run_this(cdo_command, self, output="ensemble")
        return None

    if stat not in ["mean", "sum", "min", "max", "range", "var", "cumsum", "std"]:
        raise ValueError(f"{stat} is not a valid CDO stat!")

    # some tidying of over
    if type(over) is str:
        over = [over]

    over = [x.lower() for x in over]
    over = ["month" if "mon" in x else x for x in over]
    over = ["year" if "yea" in x else x for x in over]
    over = ["season" if "sea" in x else x for x in over]

    for x in over:
        if x not in ["day", "month", "year", "season"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping over season and day and month makes no sense

    if "season" in over and ("month" in over or "day" in over):
        raise ValueError("You cannot group over season and day or month")

    over = sorted(list(set(over)))

    if over == ["day", "month"]:
        over = ["day"]

    # sort over alphabetically

    # single variables
    # daily climatology
    if over == ["day"]:
        ydaystat(self, stat = stat)
        return None

    # monthly climatology
    if over == ["month"]:
        ymonstat(self, stat = stat)
        return None

    # annual mean
    if over == ["year"]:
        yearlystat(self, stat = stat)
        return None

    # seasonal climatology
    if over == ["season"]:
        seasclim(self, stat = stat)
        return None

    # seasonal climatology
    if over == ["season", "year"]:
        seasstat(self, stat = stat)
        return None


    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        dailystat(self, stat = stat)
        return None

    # monthly mean

    if over == ["month", "year"]:
        monstat(self, stat = stat)
        return None




def tsum(self, over = "time"):
    """
    Calculate the temporal sum of all variables
    """
    time_stat(self, stat="sum", over = over)


def tmean(self, over = "time"):
    """
    Calculate the temporal mean of all variables
    """
    time_stat(self, stat="mean", over = over)


def tmin(self, over = "time"):
    """
    Calculate the temporal minimum of all variables
    """
    time_stat(self, stat="min", over = over)


def tmax(self, over = "time"):
    """
    Calculate the temporal maximum of all variables
    """
    time_stat(self, stat="max", over = over)

def tmedian(self, over = "time"):
    """
    Calculate the temporal median of all variables
    """
    self.tpercentile(p = 50, over = over)


def trange(self, over = "time"):
    """
    Calculate the temporal range of all variables
    """
    time_stat(self, stat="range", over = over)



def tvariance(self, over = "time"):
    """
    Calculate the temporal variance of all variables
    """
    time_stat(self, stat="var", over = over)

def tstdev(self, over = "time"):
    """
    Calculate the temporal standard deviation of all variables
    """
    time_stat(self, stat="std", over = over)


def tcumsum(self):
    """
    Calculate the temporal cumulative sum of all variables
    """
    # create cdo command and runit
    time_stat(self, stat="cumsum")


def tpercentile(self, p=None, over = "time"):
    """
    Calculate the temporal percentile of all variables

    Parameters
    -------------
    p: float or int
        Percentile to calculate
    """
    over = over
    if p is None:
        raise ValueError("Please supply p")

    if type(p) not in [int, float]:
        raise TypeError("p is a " + str(type(p)) + ", not int or float")

    if (p < 0) or (p > 100):
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    self.run()

    # create cdo command and run it

    if type(over) is str:
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
        min_command = " -timmin "
        max_command = " -timmax "

    # single variables
    # daily climatology
    if over == ["day"]:
        min_command = " -ydaymin "
        max_command = " -ydaymax "

    # monthly climatology
    if over == ["month"]:
        min_command = " -ymonmin "
        max_command = " -ymonmax "

    # annual mean
    if over == ["year"]:
        min_command = " -yearmin "
        max_command = " -yearmax "

    # seasonal climatology
    if over == ["season"]:
        min_command = " -yseasmin "
        max_command = " -yseasmax "

    # seasonal climatology
    if over == ["season", "year"]:
        min_command = " -seasmin "
        max_command = " -seasmax "


    # all three. This is daily mean

    if over == ["day", "month", "year"] or over == ["day", "year"]:
        min_command = " -daymin "
        max_command = " -daymax "

    # monthly mean

    if over == ["month", "year"]:
        min_command = " -monmin "
        max_command = " -monmax "


    new_files = []
    new_commands = []
    for ff in self:
        target = temp_file("nc")

        cdo_command = (
            "cdo -timpctl,"
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
        target = run_cdo(cdo_command, target)
        new_files.append(target)
        new_commands.append(cdo_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()





