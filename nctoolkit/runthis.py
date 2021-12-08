import copy
import os
import re
import subprocess
import platform
import warnings
import multiprocessing

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.session import (
    nc_protected,
    session_info,
    append_safe,
    remove_safe,
    get_protected,
)
from nctoolkit.temp_file import temp_file

from nctoolkit.show import nc_variables

from nctoolkit.utils import cdo_version


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def tidy_command(command):

    if session_info["precision"] is not None:
        command = command.replace("cdo ", "cdo -b " + session_info["precision"] + " ")

    command = command.replace("  ", " ")

    if " --sortname " in command:
        command = command.replace(" --sortname ", " ")
        command = command.replace("cdo ", "cdo --sortname ")

    if "reduce_dim" in command:
        command = (
            command.replace("reduce_dim", "").replace(" - ", " ").replace(" -- ", " ")
        )
        command = command.replace("cdo ", "cdo --reduce_dim ")

    command = command.strip()

    if session_info["thread_safe"] is False:
        command = command.replace("-L ", " ").replace("cdo ", "cdo -L ")
    else:
        command = command.replace("-L ", " ")

    return command


def run_nco(command, target, out_file=None, overwrite=False):
    command = command.strip()
    append_safe(target)
    original_target = target
    if (
        command.startswith("ncea ")
        or command.startswith("ncra ")
        or command.startswith("ncap ")
        or command.startswith("ncap2 ")
        or command.startswith("ncks ")
        or command.startswith("ncatted")
    ) is False:
        raise ValueError("This is not a valid NCO command")

    # Make sure it is not attempting to overwrite a protected file
    if out_file is None:
        if command.split()[-1] in get_protected():
            if overwrite is False:
                raise ValueError("Attempting to overwrite an opened file")

    if platform.system() == "Linux":
        if session_info["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result < 1 * 1e9:
                session_info["temp_dir"] == "/var/tmp/"
                if target.startswith("/tmp"):
                    new_target = target.replace("/tmp/", "/var/tmp/")
                    command = command.replace(target, new_target)
                    remove_safe(target)
                    target = new_target
                    append_safe(target)

    out = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    result, ignore = out.communicate()

    if "(Abort)" in str(result):
        raise ValueError(
            str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        )

    if "ERROR" in str(result):
        if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            append_safe(new_target)
            remove_safe(target)
            target = new_target

            out = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            result1, ignore = out.communicate()
            if "ERROR" in str(result1):
                remove_safe(target)
                raise ValueError(
                    str(result1).replace("b'", "").replace("\\n", "").replace("'", "")
                )
            session_info["temp_dir"] = "/var/tmp/"
            if "Warning:" in str(result1):
                warnings.warn(message=f"NCO warning: {str(result1)}")
    else:
        if "Warning:" in str(result):
            warnings.warn(message=f"NCO warning: {str(result)}")

    if target != "":
        if os.path.exists(target) is False:
            remove_safe(target)
            raise ValueError(f"{command} was not successful. Check output")
    else:
        actual_target = command.split(" ")[-1].strip()
        if os.path.exists(actual_target) is False:
            remove_safe(target)
            raise ValueError(f"{command} was not successful. Check output")

    if target != "":
        session_info["latest_size"] = os.path.getsize(target)

    return target


def run_cdo(command = None, target = None, out_file=None, overwrite=False, precision = None):


    if type(precision) is not str:
        raise ValueError("Precision must be str")
    
    if precision not in ["I8", "I16", "I32", "F32", "F64", "default"]:
        raise ValueError(f"Precision - {precision} - is not valid")
        
    if precision in ["I8", "I16", "I32", "F32", "F64"]:
        if " -b " not in command:
            command = command.replace("cdo ", f"cdo -b {precision} ")


    # make sure the output file does not exist

    command = tidy_command(command)
    start_target = target

    if out_file is None:
        if os.path.exists(command.split()[-1]):
            if overwrite is False:
                raise ValueError("Attempting to overwrite file")

    if platform.system() == "Linux":
        if session_info["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result < 1 * 1e9:
                session_info["temp_dir"] == "/var/tmp/"
                if target.startswith("/tmp"):
                    new_target = target.replace("/tmp/", "/var/tmp/")
                    command = command.replace(target, new_target)
                    target = target.replace("/tmp/", "/var/tmp/")
    append_safe(target)

    if command.startswith("cdo ") is False:
        raise ValueError("The command does not start with cdo!")

    out = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out.wait()
    result, ignore = out.communicate()

    # If it is a generic grid, it's better to not throw the CDO error which might be confusing.
    if "generic" in result.decode("utf-8").lower():
        if "unsupported" in result.decode("utf-8").lower():
            raise ValueError(
                "Dataset contains generic grids. Please fix to lonlat or curvilinear"
            )

    # this will potentially fail because of floating point precision. A quick fix to see if that is the case....
    if "Use the CDO option -b F32" in (
        result.decode("utf-8")
    ) or "not represent" in result.decode("utf-8"):
        print("Switching to 32 bit precision!")
        command_chunks = command.split(" ")

        i = 0
        change = None
        for cc in command_chunks:
            i += 1
            if "-b" == cc.strip():
                change = i
        if change is not None:
            command_chunks[change] = "32"
            command = str_flatten(command_chunks, " ")
        else:
            command = command.replace("cdo ", "cdo -b 32 ")

        if os.path.exists(target):
            if out_file is None:
                os.remove(target)
                remove_safe(target)

        new_target = temp_file("nc")
        append_safe(new_target)
        command = command.replace(target, new_target)
        target = new_target

        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out.wait()
        result, ignore = out.communicate()

    if "Use the CDO option -b F32" in (result.decode("utf-8")):
        command_chunks = command.split(" ")

        i = 0
        change = None
        for cc in command_chunks:
            i += 1
            if "-b" == cc.strip():
                change = i
        if change is not None:
            command_chunks[change] = "F32"
            command = str_flatten(command_chunks, " ")
        else:
            command = command.replace("cdo ", "cdo -b F64 ")
        command

        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out.wait()
        result, ignore = out.communicate()

    if out_file is not None:
        if "HDF5 library version mismatched error" in str(result):
            remove_safe(target)
            remove_safe(start_target)
            raise ValueError(
                "The HDF5 header files used to compile this application do not match "
                "the version used by the HDF5 library to which this application is "
                "linked. This is likely because of a conda problem."
            )

        if (
            str(result).startswith("b'Error")
            or ("HDF error" in str(result))
            or (out.returncode != 0)
        ):
            remove_safe(target)
            remove_safe(start_target)
            raise ValueError(
                str(result).replace("b'", "").replace("\\n", "").replace("'", "")
            )
        else:
            return out_file

    if ("sellonlat" in command) and ("std::bad_alloc" in str(result)):
        remove_safe(target)
        remove_safe(start_target)
        raise ValueError(
            "Is the horizontal grid very large? Consider setting cdo=False in crop!"
        )

    if "(Abort)" in str(result):
        remove_safe(target)
        remove_safe(start_target)
        raise ValueError(
            str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        )

    if "HDF5 library version mismatched error" in str(result):
        raise ValueError(
            "The HDF5 header files used to compile this application do not match "
            "the version used by the HDF5 library to which this application is "
            "linked. This is likely because of a conda problem."
        )

    if (
        (str(result).startswith("b'Error"))
        or ("HDF error" in str(result))
        or (out.returncode != 0)
    ):
        if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            target = new_target
            append_safe(target)

            out = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            out.wait()
            result1, ignore = out.communicate()
            if (
                (str(result1).startswith("b'Error"))
                or ("HDF error" in str(result1))
                or (out.returncode != 0)
            ):
                if "Too many open files" in str(result1):
                    remove_safe(target)
                    remove_safe(start_target)
                    raise ValueError(
                        "There are too many open files in CDO. Check the files "
                        "your OS allows to be open simultaneously in the Bourne "
                        "shell with 'ulimit -n'"
                    )
                else:
                    remove_safe(target)
                    remove_safe(start_target)
                    raise ValueError(
                        str(result1)
                        .replace("b'", "")
                        .replace("\\n", "")
                        .replace("'", "")
                    )
            session_info["temp_dir"] = "/var/tmp/"

            # loop through the warnings

            messages = str(result1).split("\\n")

            missing_years = []
            missing_months = []
            for x in messages:
                if "Warning:" in x:
                    print_result1 = True
                    if ("merge" in x) and ("Duplicate entry of parameter" in str(x)):
                        print_result1 = False

                    # deal with warning messages for selecting months
                    pattern = re.compile(r"Year \d{4} not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall("\d{4}", x)
                        missing_years.append(d[0])

                    pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall("([1-9][0-9]?|100)", x)
                        missing_months.append(d[0])
                    if print_result1:
                        warnings.warn(
                            message="CDO warning:"
                            + x.replace("b'Warning:", "").replace("Warning:", "")
                        )

            if len(missing_years) > 0:
                warnings.warn(
                    message=f'CDO warning: Years {str_flatten(missing_years, ",")} '
                    "are missing",
                    stacklevel=2,
                )
            if len(missing_months) > 0:
                warnings.warn(
                    message=f'CDO warning: Months {str_flatten(missing_months, ",")} '
                    "are missing",
                    stacklevel=2,
                )
    else:
        messages = str(result).split("\\n")

        missing_years = []
        missing_months = []
        for x in messages:
            if "Warning:" in x:
                print_result = True
                if ("merge" in x) and ("Duplicate entry of parameter" in str(x)):
                    print_result = False

                # deal with warning messages for selecting months
                pattern = re.compile(r"Year \d{4} not found")

                if pattern.search(x):
                    d = re.findall("\d{4}", x)
                    missing_years.append(d[0])
                    print_result = False

                pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")

                if pattern.search(x):
                    d = re.findall("([1-9][0-9]?|100)", x)
                    missing_months.append(d[0])
                    print_result = False

                if print_result:
                    warnings.warn(
                        message="CDO warning:"
                        + x.replace("b'Warning:", "").replace("Warning:", "")
                    )

        if len(missing_years) > 0:
            warnings.warn(
                message=f'CDO warning: Years {str_flatten(missing_years, ",")} '
                "are missing!",
                category=Warning,
            )
        if len(missing_months) > 0:
            warnings.warn(
                message=f'CDO warning: Months {str_flatten(missing_months, ",")} '
                "are missing",
                category=Warning,
            )

    if os.path.exists(target) is False:
        remove_safe(target)
        remove_safe(target)
        raise ValueError(f"{command} was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target


def run_this(os_command, self, output="one", out_file=None):

    if len(self) == 0:
        raise ValueError("Failure do to empty dataset!")

    self._ncommands += 1

    cores = session_info["cores"]

    if len(self) == 1:
        output = "ensemble"

    if len(self._hold_history) != len(self.history):
        if self._merged == False and len(self.history) > 0 and output == "one":

            if cdo_version() in ["9.9.9"]:
                the_command = self.history[-1].replace("cdo", "") + " "
                the_command = the_command.replace(" -L ", " ").strip()
                if "apply," not in the_command:
                    self.history[-1] = f'-apply,"{the_command}"'

    if self._execute is False:
        if len(self._hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")
            self.history[-1] = self.history[-1].replace("  ", " ")

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
                pool = multiprocessing.Pool(cores)
                target_list = []
                results = dict()
            else:
                target_list = []

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

                if self._zip and zip_copy and format_it == False:
                    ff_command = ff_command.replace("cdo ", "cdo -z zip copy ")
                else:
                    if self._zip:
                        ff_command = ff_command.replace("cdo ", "cdo -z zip ")

                new_history.append(ff_command)

                if cores > 1:
                    temp = pool.apply_async(run_cdo, [ff_command, target, out_file,  False, self._precision])
                    results[ff] = temp
                else:

                    target = run_cdo(ff_command, target, out_file, precision = self._precision)
                    target_list.append(target)

            if cores > 1:
                pool.close()
                pool.join()
                for k, v in results.items():
                    target_list.append(v.get())

            self.history = copy.deepcopy(new_history)
            self.current = copy.deepcopy(target_list)

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

        if ((output == "one") and (len(self) > 1)) or self._zip == False:

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
                    os_command = os_command.replace("cdo ", f"cdo -f {self._format} ")

            if self._zip and zip_copy and format_it == False:
                os_command = os_command.replace("cdo ", "cdo -z zip copy ")
            else:
                if self._zip:
                    os_command = os_command.replace("cdo ", "cdo -z zip ")

            if "infile09178" in os_command:
                os_command = os_command.replace(ff, "")
                os_command = os_command.replace("infile09178", ff)

            os_command = tidy_command(os_command)

            if "mergetime" in os_command:
                try:
                    target = run_cdo(os_command, target, out_file, precision = self._precision)
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
                    if (
                        "1.9.4" in cdo_version()
                        or "1.9.5" in cdo_version()
                        or "1.9.6" in cdo_version()
                        or "1.9.7" in cdo_version()
                        or "1.9.8" in cdo_version()
                    ):

                        target = run_cdo(os_command, target, out_file, precision = self._precision)
                    else:
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

                        target = run_cdo(os_command, target, out_file, precision = self._precision)
            else:
                target = run_cdo(os_command, target, out_file, precision = self._precision)

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
