
from nctoolkit.runthis import run_this


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
    ydaystat(self, stat="mean")


def daily_min_climatology(self):
    """
    Calculate a daily minimum climatology
    """
    ydaystat(self, stat="min")


def daily_max_climatology(self):
    """
    Calculate a daily maximum climatology
    """
    ydaystat(self, stat="max")


def daily_range_climatology(self):
    """
    Calculate a daily range climatology
    """
    ydaystat(self, stat="range")
