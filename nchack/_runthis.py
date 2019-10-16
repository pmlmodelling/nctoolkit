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

    if str(result).startswith("b'Error"):
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
            
    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    return target

def run_this(os_command, self, silent = False, output = "one", cores = 1, n_operations = 1):

    """Method to run an nco/cdo system command and check output was generated"""
    # Works on multiple files
    run = self.run
    # Step one

    # Step 2: run the system command
    
    if run == False:
        self.history.append(os_command)

    if run:

        if type(self.current) is str:
            if os.path.exists(self.current) == False:
                raise ValueError("The file " + self.current + " does not exist!")
            # single file case
            if silent:
                os_command = os_command.replace("cdo ", "cdo -s ")

            target = temp_file("nc") 
            nc_created.append(target)
            os_command = os_command + " " + self.current + " " + target

            run_history = [x for x in self.history if x.endswith(".nc")]
            self.history = copy.deepcopy(run_history)
            self.history.append(os_command)

            target = run_cdo(os_command, target)
            
            # check the file was actually created
            # Raise error if it wasn't

            if os.path.exists(target) == False:
                raise ValueError(os_command + " was not successful. Check output")
            self.current = target

        else:
            # multiple file case

            if output == "one":
                
                if n_operations > 128:
                    read = os.popen("cdo --operators").read()
                    cdo_methods = [x.split(" ")[0] for x in read.split("\n")]
                    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

                    # mergetime case
                    # operations after merging need to be chunked by file
                    # right now, this is only limited to mergetime
                    # I don't think there is anything else that can be chunked
                    # so the two if statements can probably be merged later
                    
                    if "mergetime " in os_command:

                        if "mergetime " in os_command:
                            merge_op = "mergetime "
                        
                        post_merge = 0
                        for x in os_command.split(merge_op)[0].split(" "):
                            for y in x.split(","):
                                if y.replace("-", "") in cdo_methods:
                                    post_merge +=1
                        n_files = len(self.current)
                        n_split = n_operations - post_merge - 1
                        max_split = 127 - post_merge
                        file_chunks = split_list(self.current, math.ceil(n_split / max_split) + 1)
                        
                        os_commands = []
                        start_chunk = os_command.split(merge_op)[1]
                        tracker = 0
                        targets = []
                        for cc in file_chunks:
                            end_file = file_chunks[tracker][-1]
                            tracker+=1
                            
                            os_commands.append(start_chunk.split(end_file)[0] + " " + end_file)
                            start_chunk = start_chunk.split(end_file)[1] 
                        
                        for x in os_commands:
                            target = temp_file("nc") 
                            a_command = "cdo -L -" + merge_op + x + " " + target
                            nc_created.append(target)
                            target = run_cdo(a_command, target)
                            
                            if os.path.exists(target) == False:
                                raise ValueError(a_command + " was not successful. Check output")
                            self.history.append(a_command)
                            targets.append(target)

                        target = temp_file("nc") 
                        a_command = "cdo -L -" + merge_op +  str_flatten(targets, " ") + " " + target
                        nc_created.append(target)
                        target = run_cdo(a_command, target)
                            
                        if os.path.exists(target) == False:
                            raise ValueError(a_command + " was not successful. Check output")
                        self.history.append(a_command)
                        
                        if post_merge > 0:
                            post_merge = os_command.split(merge_op)[0] + " " 
                            out_file  = temp_file("nc") 
                            nc_created.append(out_file)

                            post_merge = post_merge.replace(" - ", " ") + target + " " + out_file
                            out_file = run_cdo(post_merge, out_file)
                            if os.path.exists(out_file) == False:
                                raise ValueError(post_merge + " was not successful. Check output")
                            self.history.append(post_merge)
                            self.current = out_file
                        else:
                            self.current = target
                        return None
                
        
                    if "merge " in os_command:
                        if n_operations > 128:
                            raise ValueError("More than 128 operations have been chained")

                for ff in self.current:
                    if os.path.exists(ff) == False:
                        raise ValueError("The file " + ff + " does not exist!")

                if silent:
                    ff_command = os_command.replace("cdo ", "cdo -s ")
                else:
                    ff_command = copy.deepcopy(os_command)

                target = temp_file("nc") 
                nc_created.append(target)
                flat_ensemble = str_flatten(self.current, " ")
                if (self.merged == False) or (".nc" not in ff_command):
                    ff_command = ff_command + " " + flat_ensemble + " " + target
                else:
                    ff_command = ff_command + " "  + target

                run_history = copy.deepcopy(self.history)
                run_history = [x for x in run_history if x.endswith(".nc")]
                self.history = copy.deepcopy(run_history)

                if "merge" in ff_command:
                    ff_command = ff_command.replace(" merge ", " -merge ")
                    ff_command = ff_command.replace(" mergetime ", " -mergetime ")
                    #ff_command = ff_command.replace("cdo ", "cdo -z zip ")
                    ff_command = ff_command.replace(" -s ", " ")
                    ff_command = ff_command.replace("cdo ", "cdo -s ")

                self.history.append(ff_command)
                target = run_cdo(ff_command, target)
                
                # check the file was actually created
                # Raise error if it wasn't

                if os.path.exists(target) == False:
                    raise ValueError(ff_command + " was not successful. Check output")
                self.current = target

            else:
                if cores == 1:
                    target_list = []
                    for ff in self.current:
                    
                        if os.path.exists(ff) == False:
                            raise ValueError("The file " + ff + " does not exist!")
                        if silent:
                            ff_command = os_command.replace("cdo ", "cdo -s ")
                        else:
                            ff_command = copy.deepcopy(os_command)

                        target = temp_file("nc") 
                        nc_created.append(target)
                        ff_command = ff_command + " " + ff + " " + target

                        self.history.append(ff_command)
                        target = run_cdo(ff_command, target)
                        
                        # check the file was actually created
                        # Raise error if it wasn't

                        if os.path.exists(target) == False:
                            raise ValueError(ff_command + " was not successful. Check output")
                        target_list.append(target) 

                    self.current = copy.deepcopy(target_list)

                else:
                # multi-core case

                    pool = multiprocessing.Pool(cores)
                    target_list = []
                    results = dict()
                    for ff in self.current:
                    
                        if silent:
                            ff_command = os_command.replace("cdo ", "cdo -s ")
                        else:
                            ff_command = copy.deepcopy(os_command)

                        target = temp_file("nc") 
                        nc_created.append(target)
                        ff_command = ff_command + " " + ff + " " + target

                        self.history.append(ff_command)
                        temp = pool.apply_async(run_cdo,[ff_command, target])
                        results[ff] = temp 

                    pool.close()
                    pool.join()
                    new_current = []
                    for k,v in results.items():
                        target_list.append(v.get())

                    self.current = copy.deepcopy(target_list)


    else:
        # Now, if this is not a cdo command we need throw an error

        if os_command.strip().startswith("cdo") == False:
            raise ValueError("You can only use cdo commands in hold mode")
        # Now, we need to throw an error if the command is generating a grid
        
#        commas = [x for x in os_command.split(" ") if "," in x]
#        commas = "".join(commas)
#        if "gen" in commas:
#            raise ValueError("You cannot generate weights as part of a chain!")
#


