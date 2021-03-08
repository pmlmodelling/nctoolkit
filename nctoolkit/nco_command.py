import copy

from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_nco
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe


def nco_command(self, command=None, ensemble=False):
    """
    Apply an nco command

    Parameters
    -------------
    command : string
        nco command to call. This must be of a form such that
        "nco {command} infile outfile" will run.
    ensemble : boolean
        Set to True if you want the command to take all of the files as input.
        This is useful for ensemble methods.
    """

    self.run()

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if type(command) is not str:
        raise TypeError("Command supplied is not a str")

    new_files = []
    new_commands = []

    if (ensemble is False) or (len(self) == 1):
        for ff in self:

            target = temp_file(".nc")

            the_command = f"{command} {ff} {target}"

            target = run_nco(the_command, target=target)

            new_files.append(target)
            new_commands.append(the_command)

    else:
        target = temp_file(".nc")

        files = str_flatten(self.current, " ")

        the_command = f"{command} {files} {target}"

        target = run_nco(the_command, target=target)

        new_files.append(target)
        new_commands.append(the_command)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    self.history.append(command)
    self._hold_history = copy.deepcopy(self.history)

    self.disk_clean()
