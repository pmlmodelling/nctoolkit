import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.temporals import *
from nctoolkit.temp_file import temp_file
import warnings


def time_stat(self, stat="mean", by = "time"):
    """Method to calculate a stat over all time steps"""
    # create cdo command and run it
    if by == "time":
        cdo_command = f"cdo -tim{stat}"
        run_this(cdo_command, self, output="ensemble")
        return None

    if stat not in ["mean", "sum", "min", "max", "range", "var", "cumsum", "std"]:
        raise ValueError(f"{stat} is not a valid CDO stat!")

    if type(by) is str:
        by = [by]

    for x in by:
        if x not in ["day", "month", "year", "season"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping by season and day and month makes no sense

    if "season" in by and ("month" in by or "day" in by):
        raise ValueError("You cannot group by season and day or month")

    by = sorted(list(set(by)))

    if by == ["day", "month"]:
        by = ["day"]

    # sort by alphabetically

    # single variables
    # daily climatology
    if by == ["day"]:
        ydaystat(self, stat = stat)
        return None

    # monthly climatology
    if by == ["month"]:
        ymonstat(self, stat = stat)
        return None

    # annual mean
    if by == ["year"]:
        yearlystat(self, stat = stat)
        return None

    # seasonal climatology
    if by == ["season"]:
        seasclim(self, stat = stat)
        return None

    # seasonal climatology
    if by == ["season", "year"]:
        seasstat(self, stat = stat)
        return None


    # all three. This is daily mean

    if by == ["day", "month", "year"] or by == ["day", "year"]:
        dailystat(self, stat = stat)
        return None

    # monthly mean

    if by == ["month", "year"]:
        monstat(self, stat = stat)
        return None




def sum(self):
    """
    Calculate the temporal sum of all variables
    """
    time_stat(self, stat="sum")


def mean(self, by = "time"):
    """
    Calculate the temporal mean of all variables
    """
    time_stat(self, stat="mean", by = by)


def min(self, by = "time"):
    """
    Calculate the temporal minimum of all variables
    """
    time_stat(self, stat="min", by = by)


def max(self, by = "time"):
    """
    Calculate the temporal maximum of all variables
    """
    time_stat(self, stat="max", by = by)

def median(self, by = "time"):
    """
    Calculate the temporal median of all variables
    """
    self.percentile(p = 50, by = by)


def range(self, by = "time"):
    """
    Calculate the temporal range of all variables
    """
    time_stat(self, stat="range", by = by)



def variance(self, by = "time"):
    """
    Calculate the temporal variance of all variables
    """
    time_stat(self, stat="var", by = by)

def stdev(self, by = "time"):
    """
    Calculate the temporal standard deviation of all variables
    """
    time_stat(self, stat="std", by = by)


def cumsum(self):
    """
    Calculate the temporal cumulative sum of all variables
    """
    # create cdo command and runit
    time_stat(self, stat="cumsum")


def percentile(self, p=None, by = "time"):
    """
    Calculate the temporal percentile of all variables

    Parameters
    -------------
    p: float or int
        Percentile to calculate
    """
    if p is None:
        raise ValueError("Please supply p")

    if type(p) not in [int, float]:
        raise TypeError("p is a " + str(type(p)) + ", not int or float")

    if (p < 0) or (p > 100):
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    self.run()

    # create cdo command and run it

    if type(by) is str:
        by = [by]

    for x in by:
        if x not in ["day", "month", "year", "season", "time"]:
            raise ValueError(f"{x} is not a valid group!")

    #  grouping by season and day and month makes no sense

    if "season" in by and ("month" in by or "day" in by):
        raise ValueError("You cannot group by season and day or month")

    by = sorted(list(set(by)))

    if by == ["day", "month"]:
        by = ["day"]


    if by == ["time"]:
        min_command = " -timmin "
        max_command = " -timmax "

    # single variables
    # daily climatology
    if by == ["day"]:
        min_command = " -ydaymin "
        max_command = " -ydaymax "

    # monthly climatology
    if by == ["month"]:
        min_command = " -ymonmin "
        max_command = " -ymonmax "

    # annual mean
    if by == ["year"]:
        min_command = " -yearmin "
        max_command = " -yearmax "

    # seasonal climatology
    if by == ["season"]:
        min_command = " -yseasmin "
        max_command = " -yseasmax "

    # seasonal climatology
    if by == ["season", "year"]:
        min_command = " -seasmin "
        max_command = " -seasmax "


    # all three. This is daily mean

    if by == ["day", "month", "year"] or by == ["day", "year"]:
        min_command = " -daymin "
        max_command = " -daymax "

    # monthly mean

    if by == ["month", "year"]:
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





