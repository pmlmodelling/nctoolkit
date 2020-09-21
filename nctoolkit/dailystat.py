from nctoolkit.runthis import run_this


def dailystat(self, stat="mean"):
    """Function to calculate the daily statistic for a function"""

    cdo_command = f"cdo -day{stat}"

    run_this(cdo_command, self, output="ensemble")


def daily_mean(self):
    """
    Calculate the daily mean for each variable
    """
    dailystat(self, stat="mean")


def daily_min(self):
    """
    Calculate the daily minimum for each variable
    """
    dailystat(self, stat="min")


def daily_max(self):
    """
    Calculate the daily maximum for each variable
    """
    dailystat(self, stat="max")


def daily_range(self):
    """
    Calculate the daily range for each variable
    """
    dailystat(self, stat="range")


def daily_sum(self):
    """
    Calculate the daily sum for each variable
    """
    dailystat(self, stat="sum")
