import copy
import multiprocessing
import platform
import warnings

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_nco
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe, session_info, append_safe, get_safe


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

    Examples
    -------------
    Select a variable from a file
    >>> ds.nco_command("ncks -v tas")
    """

    self.run()

    if len(self) == 1:
        ensemble = False

    cores = session_info["cores"]

    if platform.system() != "Linux":
        if cores > 1:
            warnings.warn("This cannot run in parallel on macOS")
            cores = 1

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if not isinstance(command, str):
        raise TypeError("Command supplied is not a str")

    if (
        command.startswith("ncea ")
        or command.startswith("ncra ")
        or command.startswith("ncap ")
        or command.startswith("ncap2 ")
        or command.startswith("ncks ")
        or command.startswith("ncrename ")
        or command.startswith("ncatted")
    ) is False:
        raise ValueError("This is not a valid NCO command")
    new_files = []
    new_commands = []

    if cores > 1:
        pool = multiprocessing.Pool(cores)
        target_list = []
        results = dict()
    else:
        target_list = []

    if (ensemble is False) or (len(self) == 1):
        if cores > 1:
            for ff in self:
                target = temp_file(".nc")

                append_safe(target)

                the_command = f"{command} {ff} {target}"
                the_command = the_command.replace("  ", " ")

                temp = pool.apply_async(run_nco, [the_command, target])
                results[ff] = temp
                new_commands.append(the_command)

        else:
            for ff in self:
                target = temp_file(".nc")
                append_safe(target)

                the_command = f"{command} {ff} {target}"
                the_command = the_command.replace("  ", " ")

                target = run_nco(the_command, target=target)

                new_files.append(target)
                new_commands.append(the_command)

    else:
        target = temp_file(".nc")
        append_safe(target)

        files = str_flatten(self.current, " ")

        the_command = f"{command} {files} {target}"
        the_command = the_command.replace("  ", " ")

        target = run_nco(the_command, target=target)

        new_files.append(target)
        new_commands.append(the_command)

    if cores == 1 or ensemble:
        self.current = new_files

        while True:
            removed = 0
            for ff in new_files:
                if len([x for x in get_safe() if x == ff]) > 1:
                    remove_safe(ff)
                    removed += 1
            if removed == 0:
                break

        for cc in new_commands:
            self.history.append(cc)
        # self.history.append(command)
        self._hold_history = copy.deepcopy(self.history)

    if cores > 1 and ensemble is False:
        pool.close()
        pool.close()
        for k, v in results.items():
            target_list.append(v.get())

        self.current = copy.deepcopy(target_list)
        for cc in new_commands:
            self.history.append(cc)
        self._hold_history = copy.deepcopy(self.history)

        while True:
            removed = 0
            for ff in target_list:
                if len([x for x in get_safe() if x == ff]) > 1:
                    remove_safe(ff)
                    removed += 1
            if removed == 0:
                break

    self.disk_clean()
    cleanup()
