
import subprocess
import copy
from .temp_file import temp_file
from .runthis import run_nco
from .cleanup import cleanup
from .cleanup import disk_clean
from .session import nc_safe


def nco_command(self, command):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This must be of the form cdo command infile outfile, where cdo, infile and outfile are attached later.
    """

    # First, check that the command is valid

    if type(self.current) is list:
        raise TypeError("This does not yet work with ensembles!")


    if type(command) is not str:
        raise TypeError("Command supplied is not a str")


    target = temp_file(".nc")

    command = command + " " + self.current + " " + target

    target = run_nco(command, target = target)


    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target

    nc_safe.append(self.current)

    self.history.append(command)
    self._hold_history = copy.deepcopy(self.history)





    self.disk_clean()



