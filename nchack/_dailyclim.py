from ._runthis import run_this

def ydaystat(self, stat = "mean"):
    """Method to calculate daily climatologies"""

    cdo_command = "cdo -yday" + stat

    run_this(cdo_command, self, output = "ensemble")


def daily_mean_climatology(self):
    """
    Calculate a daily mean climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    """

    return ydaystat(self, stat = "mean")

def daily_min_climatology(self):
    """
    Calculate a daily minimum climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    """

    return ydaystat(self, stat = "min")

def daily_max_climatology(self):
    """
    Calculate a daily maximum climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    """
    return ydaystat(self,  stat = "max")

def daily_range_climatology(self):
    """
    Calculate a daily range climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file


    """
    return ydaystat(self, stat = "range")

