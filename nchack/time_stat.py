from .runthis import run_this
from .runthis import run_cdo
from .cleanup import cleanup
from .session import nc_safe
from .temp_file import temp_file
import os

def time_stat(self, stat = "mean"):
    """Method to calculate a stat over all time steps"""

    # create cdo command and run it
    cdo_command = "cdo -tim" + stat
    run_this(cdo_command, self,  output = "ensemble")

def sum(self):
    """
    Calculate the sum of all values.
    """

    return time_stat(self, stat = "sum")

def mean(self):
    """
    Calculate the mean of all values.
    """

    return time_stat(self, stat = "mean")

def min(self):
    """
    Calculate the minimums of all values.
    """

    return time_stat(self, stat = "min")

def max(self):
    """
    Calculate the maximums of all values.
    """

    return time_stat(self, stat = "max")

def range(self):
    """
    Calculate the ranges of all values.
    """

    return time_stat(self,stat = "range")

def var(self):
    """
    Calculate the variances of all values.
    """

    return time_stat(self, stat = "var")


def cum_sum(self):
    """
    Calculate the cumulative sums of all values.
    """

    # create cdo command and runit
    cdo_command = "cdo -timcumsum"
    run_this(cdo_command, self,  output = "ensemble")



def percentile(self, p = 50):
    """
    Calculate the percentile of all values

    Parameters
    -------------
    p: float or int
        Percentile to calculate
    """
    self.release()

    if type(self.current) is not str:
        raise TypeError("This method currently only works with single file datasets currently")

    if type(p) not in [int, float]:
         raise TypeError("p is a " + str(type(p)) +  ", not int or float")

    if p < 0 or p > 100:
        raise ValueError("p: " + p + " is not between 0 and 100!")

    target = temp_file("nc")

    cdo_command = "cdo -L -timpctl," + str(p) + " " + self.current + " -timmin " + self.current + " -timmax " + self.current + " "  + target

    target = run_cdo(cdo_command, target)

    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target

    nc_safe.append(target)

    cleanup()






