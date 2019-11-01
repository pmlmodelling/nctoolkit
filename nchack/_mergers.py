

import copy
import os
import pandas as pd
from datetime import datetime

from ._runthis import run_this


def merge(self, zip = False):

    """
    Merge a multi-file ensemble into a single file. Merging will occur based on the time steps in the first file. This will only be effective if either you want to merge files with the same times or multi-time files with single time files.

    Parameters
    -------------
    zip : boolean
        If True, the resulting netcdf files are zipped. Defaults to False. 

    """

    if type(self.current) is not list:
        raise ValueError("The current state of the dataset is not a list")

    if self.merged:
        raise ValueError("You cannot double chain merge methods!")

    # Force a release if needed
    if self.run == False:
        self.release()

#    self.sort_times()

    self.merged = True
    
    # Now, we need to check if there are duplicate variables. If there are, we need to fix that

    all_times = []
    for ff in self.current:
        ntime = int(os.popen( "cdo ntime " + ff).read().split("\n")[0])
        all_times.append(ntime)
    if len(set(all_times)) > 1:
        print("Warning: files to merge do not have the same number of time steps!")

    all_times = []
    for ff in self.current:
        cdo_result = os.popen( "cdo showtimestamp " + ff).read()
        cdo_result = cdo_result.replace("\n", "")
        cdo_result = cdo_result.split()
        cdo_result = pd.Series( (v for v in cdo_result) )
        all_times.append(cdo_result)
    all_times = [x for x in all_times if len(x) > 1]
    
    if len(set([len(x) for x in all_times])) != 1 and len(all_times) > 1: 
        print("You are trying to merge data sets with incompatible time steps")

        
    cdo_command = ("cdo -merge ")

    run_this(cdo_command, self, output = "one", zip = zip) 





def merge_time(self, zip = True):

    """
    Time-based merging of a multi-file ensemble into a single file. This method is ideal if you have the same data split over multiple files covering different data sets. 

    Parameters
    -------------
    zip : boolean
        If True, the resulting netcdf files are zipped. Defaults to False. 

    """

    lazy_merger = copy.deepcopy(self.run)

    if self.merged:
        raise ValueError("You cannot double chain merge methods!")

    if self.run == False and (len(self.history) > len(self.hold_history)):
        self.release()

    if lazy_merger == False:
        self.lazy()

    self.merged = True

    cdo_command = "cdo --sortname -mergetime "

    run_this(cdo_command, self,  output = "one", zip = zip) 


