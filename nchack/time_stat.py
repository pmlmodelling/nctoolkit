from .runthis import run_this
from .runthis import run_cdo
from .session import nc_safe
from .temp_file import temp_file
import os

def time_stat(self, stat = "mean"):
    """Method to calculate a stat over all time steps"""
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
    if self.run == False:
        self.release()

    if type(p) not in [int, float]:
         raise TypeError("p is a " + str(type(p)) +  ", not int or float")


    target = temp_file("nc")

    cdo_command = "cdo -L -timpctl," + str(p) + " " + self.current + " -timmin " + self.current + " -timmax " + self.current + " "  + target

    target = run_cdo(cdo_command, target)

    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target

    nc_safe.append(target)






