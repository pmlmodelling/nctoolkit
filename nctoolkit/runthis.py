import copy
import os
import re
import subprocess
import platform
import warnings

if platform.system() == "Linux":
    import multiprocessing as mp
else:
    import multiprocess as mp

import signal

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.session import (
    session_info,
    append_safe,
    remove_safe,
    get_protected,
)
from nctoolkit.temp_file import temp_file

from nctoolkit.show import nc_variables
from nctoolkit.runners import run_cdo, tidy_command, run_nco


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


# pool = mp.get_context('fork').Pool(1)


def run_this(os_command, self, output="one", out_file=None, suppress=False):
    from tqdm import tqdm

    if len(self) == 0:
        raise ValueError("Failure do to empty dataset!")

    self._ncommands += 1

    cores = session_info["cores"]

    if len(self) == 1:
        output = "ensemble"

    if self._execute is False:
        if len(self._hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")
            self.history[-1] = self.history[-1].replace("  ", " ")
    try:
        if self._execute:
            if ((output == "ensemble") and (len(self) > 1)) or (
                (output == "ensemble") and (len(self) == 1)
            ):
                new_history = copy.deepcopy(self._hold_history)

                if len(self) == 1:
                    cores = 1
                file_list = self.current

                if len(self.history) > len(self._hold_history):
                    os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                    os_command = os_command.replace("  ", " ")

                if cores > 1:
                    original_sigint_handler = signal.signal(
                        signal.SIGTERM, signal.SIG_IGN
                    )
                    pool = mp.get_context('fork').Pool(cores)
                    signal.signal(signal.SIGTERM, original_sigint_handler)

                    target_list = []
                    results = dict()
                else:
                    target_list = []

                progress_bar = False

                if self._thredds is False:
                    if self.size["Number of files in ensemble"] >= 12:
                        if self.size["Ensemble size"].split(" ")[1] == "GB":
                            if float(self.size["Ensemble size"].split(" ")[0]) > 12:
                                progress_bar = True

                if session_info["progress"] == "off":
                    progress_bar = False

                if session_info["progress"] == "on" and len(self) > 1:
                    progress_bar = True

                if cores == 1:
                    if progress_bar:
                        if session_info["progress"] == "on":
                            if not suppress:
                                print("Processing ensemble! In progress:")
                        else:
                            if not suppress:
                                print("Processing large ensemble! In progress")
                        if not suppress:
                            pbar = tqdm(total=len(file_list), position=0, leave=True)

                for ff in file_list:
                    ff_command = os_command

                    ff_command = f"{ff_command} {ff} "
                    if "infile09178" in ff_command:
                        ff_command = " ".join(ff_command.split(" ")[:-2])
                        ff_command = ff_command.replace("infile09178", ff)

                    target = temp_file("nc")

                    if out_file is not None:
                        target = out_file

                    ff_command = f"{ff_command} {target}"
                    ff_command = ff_command.replace("  ", " ")
                    if " --sortname " in os_command:
                        os_command = os_command.replace(" --sortname ", " ")
                        os_command = os_command.replace("cdo  ", "cdo --sortname ")

                    if "reduce_dim" in ff_command:
                        ff_command = (
                            ff_command.replace("reduce_dim", "")
                            .replace(" - ", " ")
                            .replace(" -- ", " ")
                        )
                        ff_command = ff_command.replace("cdo ", "cdo --reduce_dim ")

                    ff_command = tidy_command(ff_command)

                    zip_copy = False
                    if self._zip and self._ncommands == 1:
                        zip_copy = True

                    format_it = False
                    if self._format is not None:
                        format_it = True
                        if self._ncommands == 1:
                            ff_command = ff_command.replace(
                                "cdo ", f"cdo -f {self._format} copy "
                            )
                        else:
                            ff_command = ff_command.replace(
                                "cdo ", f"cdo -f {self._format} "
                            )
                    ff_command = ff_command.replace(
                        "cdo ", f"cdo {self._align} "
                    ).replace("  ", " ")

                    if self._zip and zip_copy and format_it is False:
                        ff_command = ff_command.replace("cdo ", "cdo -z zip copy ")
                    else:
                        if self._zip:
                            ff_command = ff_command.replace("cdo ", "cdo -z zip ")

                    new_history.append(ff_command)

                    if cores > 1:
                        temp = pool.apply_async(
                            run_cdo,
                            [ff_command, target, out_file, False, self._precision],
                        )

                        results[ff] = temp
                    else:
                        target = run_cdo(
                            ff_command, target, out_file, precision=self._precision
                        )
                        target_list.append(target)
                        if progress_bar:
                           if not suppress:
                               pbar.update(1)

                if cores > 1:
                   if progress_bar:
                       if session_info["progress"] == "on":
                           if not suppress:
                               print("Processing ensemble. In progress:")
                       else:
                           if not suppress:
                               print("Processing a large ensemble. In progress:")
                       if not suppress:
                          pbar = tqdm(total=len(file_list), position=0, leave=True)
                   for k, v in results.items():
                       target_list.append(v.get())
                       if progress_bar:
                          if not suppress:
                              pbar.update(1)
                #if cores > 1:
                #    pool.close()


                self.history = copy.deepcopy(new_history)
                self.current = copy.deepcopy(target_list)
                self.current = [x for x in self.current if x is not None]

                if cores == 1 or session_info["parallel"]:
                    for ff in target_list:
                        remove_safe(ff)

                self.disk_clean()

                cleanup()

                self._hold_history = copy.deepcopy(self.history)

                self._zip = False

                self._ncommands = 0

                self._format = None

                return None

            if ((output == "one") and (len(self) > 1)) or self._zip is False:
                new_history = copy.deepcopy(self._hold_history)

                if len(self.history) > len(self._hold_history):
                    os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                    os_command = os_command.replace("  ", " ")

                # ensure there is sufficient space in /tmp if it is to be used
                if platform.system() == "Linux":
                    all_sizes = 0

                    for ff in self:
                        if file_size(ff) is not None:
                            all_sizes += file_size(ff)

                    result = os.statvfs("/tmp/")
                    result = result.f_frsize * result.f_bavail

                    if result < (2 * all_sizes):
                        session_info["temp_dir"] == "/var/tmp/"

                target = temp_file("nc")

                if out_file is not None:
                    target = out_file

                os_command = (
                    os_command + " [ " + str_flatten(self.current, " ") + " ] " + target
                )

                zip_copy = False
                if self._zip and self._ncommands == 1:
                    zip_copy = True

                format_it = False

                if self._format is not None:
                    format_it = True
                    if self._ncommands == 1:
                        os_command = os_command.replace(
                            "cdo ", f"cdo -f {self._format} copy "
                        )
                    else:
                        os_command = os_command.replace(
                            "cdo ", f"cdo -f {self._format} "
                        )

                if self._zip and zip_copy and format_it is False:
                    os_command = os_command.replace("cdo ", "cdo -z zip copy ")
                else:
                    if self._zip:
                        os_command = os_command.replace("cdo ", "cdo -z zip ")

                if "infile09178" in os_command:
                    os_command = os_command.replace(ff, "")
                    os_command = os_command.replace("infile09178", ff)

                os_command = tidy_command(os_command)

                os_command = os_command.replace("cdo ", f"cdo {self._align} ").replace(
                    "  ", " "
                )

                if "mergetime" in os_command:
                    try:
                        target = run_cdo(
                            os_command, target, out_file, precision=self._precision
                        )
                    except:
                        var_list = []
                        var_com = []

                        for ff in self:
                            var_list += nc_variables(ff)
                            var_com.append(nc_variables(ff))
                        new_list = []

                        for var in set(var_list):
                            if len(var_com) == len([x for x in var_com if var in x]):
                                new_list.append(var)
                        if True:
                            f_list = ",".join(new_list)
                            os_command = os_command.replace(
                                "-mergetime ", f'-mergetime -apply,"-selname,{f_list}" '
                            )

                            removed = ",".join(
                                [x for x in set(var_list) if x not in new_list]
                            )
                            if len([x for x in set(var_list) if x not in new_list]) > 0:
                                warnings.warn(
                                    f"The following variables are not in all files, so were ignored when merging: {removed}"
                                )

                            target = run_cdo(
                                os_command, target, out_file, precision=self._precision
                            )
                else:
                    target = run_cdo(
                        os_command, target, out_file, precision=self._precision
                    )

                remove_safe(target)

                self.current = target

                self.history = new_history
                self.history.append(os_command)

                self.disk_clean()

                cleanup()

                self._hold_history = copy.deepcopy(self.history)

                self._zip = False
                self._n_commands = 0

                self._format = None
    except Exception as e:
        self.reset()
        raise ValueError(e)
