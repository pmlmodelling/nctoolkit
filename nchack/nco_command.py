
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
        ff_list = self.current
    else:
        ff_list = [self.current]

    if type(command) is not str:
        raise TypeError("Command supplied is not a str")


    new_files = []
    new_commands = []


    for ff in ff_list:

        target = temp_file(".nc")

        the_command = command + " " + ff + " " + target

        target = run_nco(the_command, target = target)

        new_files.append(target)
        new_commands.append(the_command)


    for ff in new_files:
        if ff in nc_safe:
            nc_safe.remove(ff)

    self.current = new_files

    for ff in self.current:
        nc_safe.append(ff)

    if len(self.current) == 1:
        self.current = self.current[0]

    self.history.append(command)
    self._hold_history = copy.deepcopy(self.history)





    self.disk_clean()



