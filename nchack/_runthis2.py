import os
import copy
import multiprocessing
import math
import subprocess

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._session import session_stamp
from ._session import session_info


def split_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def run_cdo(command, target):
    command = command.strip()
    if command.startswith("cdo ") == False:
        raise ValueError("The command does not start with cdo!")

    out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    result,ignore = out.communicate()

    if "(Abort)" in str(result):
        raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))

    if str(result).startswith("b'Error") or "HDF error" in str(result):
       if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/") 
            command = command.replace(target, new_target)
            target = new_target
            nc_created.append(target)
            out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            result1,ignore = out.communicate()
            if str(result1).startswith("b'Error"):
                raise ValueError(str(result).replace("b'","").replace("\\n", "").replace("'", ""))
            session_stamp["temp_dir"] = "/var/tmp/"
            if "Warning:" in str(result1):
                print("CDO warning:" + str(result1))
    else:
        if "Warning:" in str(result):
            print("CDO warning:" + str(result))
            
    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target

def run_this2(os_command, self, silent = False, output = "one", cores = 1, n_operations = 1, zip = False):

    if self.run == False:
        run_commands = [x for x in self.history if x.endswith(".nc")]
        new_commands = [x for x in self.history if x.endswith(".nc") == False]
        new_commands = str_flatten(new_commands) 
        self.history = run_commands
        self.history.append(new_commands)


    if self.run:
        ####################  
        # Case 1: only one files
        ####################  

        if type(self.current) == str:
            pass

        ####################  
        # Case 2: multiple-files. Operations on everything 
        ####################  

        if type(self.current) == list and output != "one:
            pass


        ####################
        # Case 3: multiple-files. Single file output 
        ####################  


        if type(self.current) == list and output == "one:
            pass


