
import os
import copy

from ._cleanup import cleanup
from ._runthis import run_this

def release(self, silent = True, cores = 1, run_merge = True):
    """
    Run commands on tracker set to lazy/hold mode 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 
    run_merge: boolean
        Ignore this for now. This needs to be replaced by the keywords arg method

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with commands applies 
    """

    # the first step is to set the run status to true
    if self.run:
        return("Warning: tracker is in run mode. Nothing to release")

    if self.run == False:
        self.run = True

        if (len(self.history) > len(self.hold_history)):
            cdo_command = "cdo -L"
        else:
            cdo_command = "cdo "

        output_method = "ensemble"
        
        if self.merged:
            output_method = "one"

        run_this(cdo_command, self, silent, output = output_method, cores = cores)



