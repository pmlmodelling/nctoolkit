

import os
import pandas as pd

from ._cleanup import cleanup
from ._runthis import run_this


def merge(self, silent = True, zip = False):

    """
    Merge a multi-file ensemble into a single file. Merging will occur based on the time steps in the first file. This will only be effective if either you want to merge files with the same times or multi-time files with single time files.

    Parameters
    -------------
    zip : boolean
        If True, the resulting netcdf files are zipped. Defaults to False. 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with merged data. 
    """
    # OK. You have to force a release
    if self.run == False:
        self.release()

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    self.merged = True
    if "merge " in self.history or "mergetime " in self.history:
        raise ValueError("You cannot double chain merge methods!")

    # add a check for the number of operations 
   # if self.run == False:
   #     if (len(self.current) * (len(self.history) - len(self.hold_history))) > 127:
   #         raise ValueError("You cannot chain more than 128 operations in CDO. Consider releasing the tracker prior to merging!")

    
    # Now, we need to check if there are duplicate variables. If there are, we need to fix that

    all_times = []
    for ff in self.current:
        ntime = int(os.popen( "cdo ntime " + ff).read().split("\n")[0])
        all_times.append(ntime)
    if len(set(all_times)) > 1:
        print("Warning: files to merge do not have the same number of time steps!")


    all_times = []
    for ff in self.current:
        ntime = os.popen( "cdo showtimestamp " + ff).read()
        all_times.append(ntime)
    if len(set(all_times)) > 1:
        print("Warning: files to merge do not have the same times!")


    all_codes = []
    for ff in self.current:
        cdo_result = os.popen( "cdo showcode " + ff).read().replace("\n", "").strip()
        all_codes.append(cdo_result)

    if len(set(all_codes)) > len(all_codes):

        cdo_all = []
        for ff in (self.current):
            cdo_result = os.popen( "cdo codetab " + ff).read().replace("\n", "").strip().split(" ")
            cdo_result = [ff for ff in cdo_result if len(ff) > 0]
            cdo_all.append(pd.DataFrame({"code":[cdo_result[0]],"parameter": [cdo_result[1]], "path":[ff]}))
        orig_paths = pd.concat(cdo_all)
        cdo_all = pd.concat(cdo_all).drop(columns = "path").drop_duplicates()

        cdo_all["new"] = [str(ff) for ff in list(range(-len(cdo_all), 0))]


        # check length of ensemble

        cdo_command = ""

        if len(self.current) > 128/2:
            pass
        else:
            for ff in self.current:
                ff_data = (orig_paths.merge(cdo_all)
                .query("path == @ff")
                .query("code != new")
                .reset_index()
                )
                if len(ff_data) > 0:
                    sub_command = "-chcode"
                    for i in range(0, len(ff_data)):
                        sub_command+= "," + ff_data["code"][i] + "," +  ff_data["new"][i]
                    cdo_command+= " " + sub_command + " " + ff + " "
                
                if len(ff_data) == 0:
                    cdo_command += " " + ff + " "
        
        cdo_command = "cdo -L -merge " + cdo_command
        self.history.append(cdo_command)

        run_this(cdo_command, self, silent, output = "one") 

        return None
        
    cdo_command = ("cdo -merge ")

    self.history.append(cdo_command)

   # if self.run:
    run_this(cdo_command, self, silent, output = "one", zip = zip) 
   # else:
        #self.release(run_merge = False)

    # clean up the directory
    cleanup(keep = self.current)


def merge_time(self, silent = True, zip = True):

    """
    Time-based merging of a multi-file ensemble into a single file. This method is ideal if you have the same data split over multiple files covering different data sets. 

    Parameters
    -------------
    zip : boolean
        If True, the resulting netcdf files are zipped. Defaults to False. 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with merged data. 
    """

    if "merge " in self.history or "mergetime " in self.history:
        raise ValueError("You cannot double chain merge methods!")

    self.merged = True
    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo -mergetime "

    self.history.append(cdo_command)

    if self.run:
        run_this(cdo_command, self, silent, output = "one", zip = zip) 
    else:
        self.release(run_merge = False)


    # clean up the directory
    cleanup(keep = self.current)

