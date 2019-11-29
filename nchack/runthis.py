import os
import warnings
import copy
import multiprocessing
import math
import subprocess
import re
import sys

from .temp_file import temp_file
from .cleanup import cleanup
from .session import nc_safe
from .flatten import str_flatten
from .session import session_info


def split_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def run_nco(command, target, out_file = None):
    command = command.strip()
    if (command.startswith("ncea ") or command.startswith("ncra ") or command.startswith("ncatted")) == False:
        raise ValueError("This is not a valid NCO command")

    out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    result,ignore = out.communicate()


    if "(Abort)" in str(result):
        raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))

    if "ERROR" in str(result):
       if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            target = new_target
            out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            result1,ignore = out.communicate()
            if "ERROR" in str(result1):
                raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))
            session_info["temp_dir"] = "/var/tmp/"
            if "Warning:" in str(result1):
                warnings.warn(message = "NCO warning:" + str(result1))
    else:
        if "Warning:" in str(result):
            warnings.warn(message = "NCO warning:" + str(result))

    if target != "":
        if os.path.exists(target) == False:
            raise ValueError(command + " was not successful. Check output")
    else:
        actual_target = command.split(" ")[-1].strip()
        if os.path.exists(actual_target) == False:
            raise ValueError(command + " was not successful. Check output")

    if target != "":
        session_info["latest_size"] = os.path.getsize(target)

    return target


def run_cdo(command, target, out_file = None):
    command = command.strip()
    if command.startswith("cdo ") == False:
        raise ValueError("The command does not start with cdo!")

    out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out.wait()
    result,ignore = out.communicate()


    if out_file is not None:
        if str(result).startswith("b'Error") or "HDF error" in str(result) or out.returncode != 0:
            raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))
        else:
            return out_file

    if "sellonlat" in command and "std::bad_alloc" in str(result):
        raise ValueError("Is the horizontal grid very large? Consider setting cdo=False in clip!")

    if "(Abort)" in str(result):
        raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))

    if str(result).startswith("b'Error") or "HDF error" in str(result) or out.returncode != 0:
       if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            target = new_target

            out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            out.wait()
            result1,ignore = out.communicate()
            if str(result1).startswith("b'Error") or "HDF error" in str(result1) or out.returncode != 0:
                if "Too many open files" in str(result1):
                    raise ValueError("There are too many open files in CDO.  Check the files your OS allows to be open simultaneously in the Bourne shell with 'ulimit -n'")
                else:
                    raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))
            session_info["temp_dir"] = "/var/tmp/"

            # loop through the warnings

            messages = str(result1).split("\\n")

            missing_years = []
            missing_months= []
            for x in messages:
                if "Warning:" in x:
                    print_result1 = True
                    if "merge" in x and "Duplicate entry of parameter" in str(x):
                        print_result1 = False

                    # deal with warning messages for selecting months
                    pattern = re.compile(r"Year \d{4} not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall('\d{4}', x)
                        missing_years.append(d[0])

                    pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall('([1-9][0-9]?|100)', x)
                        missing_months.append(d[0])
                    if print_result1:
                        warnings.warn(message = "CDO warning:" + x.replace("b'Warning:", "").replace("Warning:",""))

            if len(missing_years) >0:
                warnings.warn(message = "CDO warning: Years " + str_flatten(missing_years, ",") + " are missing", stacklevel = 2)
            if len(missing_months) >0:
                warnings.warn(message = "CDO warning: Months " + str_flatten(missing_months, ",") + " are missing", stacklevel = 2)
    else:
        messages = str(result).split("\\n")

        missing_years = []
        missing_months = []
        for x in messages:
            if "Warning:" in x:
                print_result = True
                if "merge" in x and "Duplicate entry of parameter" in str(x):
                    print_result = False

                # deal with warning messages for selecting months
                pattern = re.compile(r"Year \d{4} not found")

                if pattern.search(x):
                    d = re.findall('\d{4}', x)
                    missing_years.append(d[0])
                    print_result = False

                pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")

                if pattern.search(x):
                    d = re.findall('([1-9][0-9]?|100)', x)
                    missing_months.append(d[0])
                    print_result = False

                if print_result:
                    warnings.warn(message = "CDO warning:" + x.replace("b'Warning:", "").replace("Warning:", ""))

        if len(missing_years) >0:
            warnings.warn(message = "CDO warning: Years " + str_flatten(missing_years, ",") + " are missing!", category = Warning)
        if len(missing_months) >0:
            warnings.warn(message = "CDO warning: Months " + str_flatten(missing_months, ",") + " are missing", category = Warning)

    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target




def run_this(os_command, self, output = "one",  out_file = None):


    cores = session_info["cores"]
    if type(cores) is not int:
        raise ValueError("cores is " + cores + ", not an int. Fix using options!")

    start_files = copy.deepcopy(self.current)

    if type(self.current) is str:
        output = "ensemble"

#    if session_info["lazy"]
    if self._run == False:
        if len(self._hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")
            self.history[-1] = self.history[-1].replace("  ", " ")

    if self._run:

        if (output == "ensemble" and type(self.current) == list) or (output == "ensemble" and type(self.current) == str):
            new_history = copy.deepcopy(self._hold_history)

            if type(self.current) == str:
                file_list = [self.current]
                cores = 1
            else:
                file_list = self.current

            if len(self.history) > len(self._hold_history):
                os_command = os_command + " " + self.history[-1].replace("cdo ", " ")
                os_command = os_command.replace("  ", " ")

            pool = multiprocessing.Pool(cores)
            target_list = []
            results = dict()

            self.history = new_history

            for ff in file_list:
                ff_command = os_command

                target = temp_file("nc")

                if out_file is not None:
                    target = out_file
                ff_command = ff_command + " " + ff + " " + target
                ff_command = ff_command.replace("  ", " ")

                self.history.append(ff_command)
                temp = pool.apply_async(run_cdo,[ff_command, target, out_file])
                results[ff] = temp

            pool.close()
            pool.join()
            new_current = []
            for k,v in results.items():
                target_list.append(v.get())

            if type(self.current) == str:
                target_list = target_list[0]

            self.current = copy.deepcopy(target_list)

            if type(self.current) is str:
                nc_safe.append(self.current)
            else:
                for ff in self.current:
                    nc_safe.append(ff)

            if type(start_files) is str:
                if start_files in nc_safe:
                    nc_safe.remove(start_files)
            else:
                for ff in start_files:
                    if ff in nc_safe:
                        nc_safe.remove(ff)

            self.disk_clean()

            if self._run:
                cleanup()
            self._hold_history = copy.deepcopy(self.history)

            return None


        if (output == "one" and type(self.current) == list):

            new_history = copy.deepcopy(self._hold_history)

            file_list = [self.current]

            if len(self.history) > len(self._hold_history):
                os_command = os_command + " " + self.history[-1].replace("cdo ", " ")
                os_command = os_command.replace("  ", " ")

            target = temp_file("nc")
            if out_file is not None:
                target = out_file
            os_command = os_command + " " +  str_flatten(self.current, " ") + " " + target
            os_command = os_command.replace("  ", " ")

            if " --sortname " in os_command:
                os_command = os_command.replace(" --sortname ", " ")
                if "cdo -L" in os_command:
                    os_command = os_command.replace("cdo -L ", "cdo -L --sortname ")
                else:
                    os_command = os_command.replace("cdo ", "cdo -L --sortname ")



            target = run_cdo(os_command, target, out_file)
            self.current = target
            self.history = new_history
            self.history.append(os_command)


            if type(self.current) is str:
                nc_safe.append(copy.deepcopy(self.current))
            else:
                for ff in self.current:
                    nc_safe.append(ff)

            if type(start_files) is str:
                if start_files in nc_safe:
                    nc_safe.remove(start_files)
            else:
                for ff in start_files:
                    if ff in nc_safe:
                        nc_safe.remove(ff)

            if self._run == True:
                self.disk_clean()

            if self._run:
                cleanup()

            self._hold_history = copy.deepcopy(self.history)


