import copy
import multiprocessing

from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_nco
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe, session_info, append_safe


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

    cores = session_info["cores"]

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

    if cores >= 1:
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

                temp = pool.apply_async(
                        run_nco, [the_command, target]
                    )
                results[ff] = temp
                new_commands.append(the_command)

        else:
            for ff in self:

                target = temp_file(".nc")
                append_safe(target)

                the_command = f"{command} {ff} {target}"

                target = run_nco(the_command, target=target)

                new_files.append(target)
                new_commands.append(the_command)

    else:
        target = temp_file(".nc")
        append_safe(target)

        files = str_flatten(self.current, " ")

        the_command = f"{command} {files} {target}"

        target = run_nco(the_command, target=target)

        new_files.append(target)
        new_commands.append(the_command)

    if cores == 1 or ensemble:

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)
        for ff in new_files:
            remove_safe(ff)

        self.history.append(command)
        self._hold_history = copy.deepcopy(self.history)




    if cores > 1:
        pool.close()
        pool.close()
        for k, v in results.items():
            target_list.append(v.get())

        self.current = copy.deepcopy(target_list)
        for cc in new_commands:
            self.history.append(cc)
        self._hold_history = copy.deepcopy(self.history)

        for ff in target_list:
            remove_safe(ff)
        for ff in target_list:
            remove_safe(ff)



    self.disk_clean()
