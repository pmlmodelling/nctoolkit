from .runthis import run_this


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

    return ydaystat(self, stat="mean")


def daily_min_climatology(self):
    """
    Calculate a daily minimum climatology
    """

    return ydaystat(self, stat="min")


def daily_max_climatology(self):
    """
    Calculate a daily maximum climatology
    """

    return ydaystat(self, stat="max")


def daily_range_climatology(self):
    """
    Calculate a daily range climatology
    """

    return ydaystat(self, stat="range")
