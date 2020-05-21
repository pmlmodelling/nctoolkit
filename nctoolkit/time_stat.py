
import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.session import nc_safe
from nctoolkit.temp_file import temp_file


def time_stat(self, stat="mean"):
    """Method to calculate a stat over all time steps"""

    # create cdo command and run it
    cdo_command = f"cdo -tim{stat}"
    run_this(cdo_command, self, output="ensemble")


def sum(self):
    """
    Calculate the temporal sum of all variables
    """
    time_stat(self, stat="sum")


def mean(self):
    """
    Calculate the temporal mean of all variables
    """
    time_stat(self, stat="mean")


def min(self):
    """
    Calculate the temporal minimum of all variables
    """
    time_stat(self, stat="min")


def max(self):
    """
    Calculate the temporal maximum of all variables
    """
    time_stat(self, stat="max")


def range(self):
    """
    Calculate the temporal range of all variables
    """
    time_stat(self, stat="range")


def var(self):
    """
    Calculate the temporal variance of all variables
    """
    time_stat(self, stat="var")


def cum_sum(self):
    """
    Calculate the temporal cumulative sum of all variables
    """
    # create cdo command and runit
    cdo_command = "cdo -timcumsum"
    run_this(cdo_command, self, output="ensemble")


def percentile(self, p=None):
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

    new_files = []
    new_commands = []
    for ff in self:
        target = temp_file("nc")

        cdo_command = (
            "cdo -timpctl,"
            + str(p)
            + " "
            + ff
            + " -timmin "
            + ff
            + " -timmax "
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
