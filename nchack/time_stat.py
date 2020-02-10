from .runthis import run_this
from .runthis import run_cdo
from .cleanup import cleanup
from .session import nc_safe
from .temp_file import temp_file
import os
import copy

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



    if type(p) not in [int, float]:
         raise TypeError("p is a " + str(type(p)) +  ", not int or float")

    if p < 0 or p > 100:
        raise ValueError("p: " + str(p) + " is not between 0 and 100!")

    if type(self.current) is list:
        ff_list = self.current
    else:
        ff_list = [self.current]

    new_files = []
    new_commands = []
    for ff in ff_list:
        target = temp_file("nc")

        cdo_command = "cdo -L -timpctl," + str(p) + " " + ff + " -timmin " + ff + " -timmax " + ff + " "  + target

        target = run_cdo(cdo_command, target)
        new_files.append(target)
        new_commands.append(cdo_command)

    self.history+=new_commands
    self._hold_history = copy.deepcopy(self.history)

    for ff in self.current:
        if ff in nc_safe:
            nc_safe.remove(ff)

    self.current = new_files

    for ff in new_files:
        nc_safe.append(ff)

    if len(self.current) == 1:
        self.current = self.current[0]

    cleanup()






