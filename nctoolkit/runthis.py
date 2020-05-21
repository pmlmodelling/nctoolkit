
import copy
import os
import re
import subprocess
import sys
import warnings
import multiprocessing

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.session import nc_safe, nc_protected, session_info
from nctoolkit.temp_file import temp_file


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

    if session_info["thread_safe"] == False:
        command = command.replace("-L ", " ").replace("cdo ", "cdo -L ")
    else:
        command = command.replace("-L ", " ")

    return command


def run_nco(command, target, out_file=None, overwrite=False):
    command = command.strip()
    if (
        command.startswith("ncea ")
        or command.startswith("ncra ")
        or command.startswith("ncatted")
    ) == False:
        raise ValueError("This is not a valid NCO command")

    # Make sure it is not attempting to overwrite a protected file
    if out_file is None:
        if command.split()[-1] in nc_protected:
            if overwrite == False:
                raise ValueError("Attempting to overwrite an opened file")

    if session_info["temp_dir"] == "/tmp/":
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail

        if result < 1 * 1e9:
            session_info["temp_dir"] == "/var/tmp/"
            if target.startswith("/tmp"):
                new_target = target.replace("/tmp/", "/var/tmp/")
                command = command.replace(target, new_target)
                target = target.replace("/tmp/", "/var/tmp/")

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
        if os.path.exists(target) == False:
            raise ValueError(f"{command} was not successful. Check output")
    else:
        actual_target = command.split(" ")[-1].strip()
        if os.path.exists(actual_target) == False:
            raise ValueError(f"{command} was not successful. Check output")

    if target != "":
        session_info["latest_size"] = os.path.getsize(target)

    return target


def run_cdo(command, target, out_file=None, overwrite=False):

    # make sure the output file does not exist

    command = tidy_command(command)

    if out_file is None:
        if os.path.exists(command.split()[-1]):
            if overwrite == False:
                raise ValueError("Attempting to overwrite file")

    if session_info["temp_dir"] == "/tmp/":
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail

        if result < 1 * 1e9:
            session_info["temp_dir"] == "/var/tmp/"
            if target.startswith("/tmp"):
                new_target = target.replace("/tmp/", "/var/tmp/")
                command = command.replace(target, new_target)
                target = target.replace("/tmp/", "/var/tmp/")

    if command.startswith("cdo ") == False:
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

    if out_file is not None:
        if "HDF5 library version mismatched error" in str(result):
            raise ValueError(
                "The HDF5 header files used to compile this application do not matchthe version used by the HDF5 library to which this application is linked. This is likely because of a conda problem."
            )

        if (
            str(result).startswith("b'Error")
            or ("HDF error" in str(result))
            or (out.returncode != 0)
        ):
            raise ValueError(
                str(result).replace("b'", "").replace("\\n", "").replace("'", "")
            )
        else:
            return out_file

    if ("sellonlat" in command) and ("std::bad_alloc" in str(result)):
        raise ValueError(
            "Is the horizontal grid very large? Consider setting cdo=False in clip!"
        )

    if "(Abort)" in str(result):
        raise ValueError(
            str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        )

    if "HDF5 library version mismatched error" in str(result):
        raise ValueError(
            "The HDF5 header files used to compile this application do not matchthe version used by the HDF5 library to which this application is linked. This is likely because of a conda problem."
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
                    raise ValueError(
                        "There are too many open files in CDO.  Check the files your OS allows to be open simultaneously in the Bourne shell with 'ulimit -n'"
                    )
                else:
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
                    message=f'CDO warning: Years {str_flatten(missing_years, ",")} are missing',
                    stacklevel=2,
                )
            if len(missing_months) > 0:
                warnings.warn(
                    message=f'CDO warning: Months {str_flatten(missing_months, ",")} are missing',
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
                message=f'CDO warning: Years {str_flatten(missing_years, ",")} are missing!',
                category=Warning,
            )
        if len(missing_months) > 0:
            warnings.warn(
                message=f'CDO warning: Months {str_flatten(missing_months, ",")} are missing',
                category=Warning,
            )

    if os.path.exists(target) == False:
        raise ValueError(f"{command} was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target


def run_this(os_command, self, output="one", out_file=None):

    cores = session_info["cores"]

    if type(self.current) is str:
        output = "ensemble"

    if self._execute == False:
        if len(self._hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")
            self.history[-1] = self.history[-1].replace("  ", " ")

    if self._execute:

        if ((output == "ensemble") and (type(self.current) == list)) or (
            (output == "ensemble") and (type(self.current) == str)
        ):
            new_history = copy.deepcopy(self._hold_history)

            if type(self.current) == str:
                file_list = [self.current]
                cores = 1
            else:
                file_list = self.current

            if len(self.history) > len(self._hold_history):
                os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                os_command = os_command.replace("  ", " ")

            pool = multiprocessing.Pool(cores)
            target_list = []
            results = dict()

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

                if self._zip:
                    ff_command = ff_command.replace("cdo ", "cdo -z zip ")

                new_history.append(ff_command)
                temp = pool.apply_async(run_cdo, [ff_command, target, out_file])
                results[ff] = temp

            pool.close()
            pool.join()
            new_current = []
            for k, v in results.items():
                target_list.append(v.get())

            if type(self.current) == str:
                target_list = target_list[0]

            self.history = copy.deepcopy(new_history)
            self.current = copy.deepcopy(target_list)

            self.disk_clean()

            cleanup()
            self._hold_history = copy.deepcopy(self.history)

            return None

        if (output == "one") and (type(self.current) == list):

            new_history = copy.deepcopy(self._hold_history)

            file_list = [self.current]

            if len(self.history) > len(self._hold_history):
                os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                os_command = os_command.replace("  ", " ")

            # ensure there is sufficient space in /tmp if it is to be used
            all_sizes = 0

            for ff in self:
                all_sizes += file_size(ff)

            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result < (2 * all_sizes):
                session_info["temp_dir"] == "/var/tmp/"

            target = temp_file("nc")

            if out_file is not None:
                target = out_file

            os_command = (
                os_command + " " + str_flatten(self.current, " ") + " " + target
            )
            if self._zip:
                os_command = os_command.replace("cdo ", "cdo -z zip ")

            if "infile09178" in os_command:
                os_command = os_command.replace(ff, "")
                os_command = os_command.replace("infile09178", ff)

            os_command = tidy_command(os_command)

            target = run_cdo(os_command, target, out_file)
            self.current = target
            self.history = new_history
            self.history.append(os_command)

            self.disk_clean()

            cleanup()

            self._hold_history = copy.deepcopy(self.history)
