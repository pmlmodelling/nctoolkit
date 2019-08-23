
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools
import copy

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def release(self, silent = True):
    """Function to release a self from hold mode  """
    # the first step is to set the run status to true
    if self.run:
        print("Warning: tracker is in run mode. Nothing to release")

    if self.run == False:
        self.run = True
        read = os.popen("cdo --operators").read()
        cdo_methods = [x.split(" ")[0] for x in read.split("\n")]
        cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]
        
        pre_history = copy.deepcopy(self.hold_history)
        
        the_history = copy.deepcopy(self.history)
        
        the_history = the_history[len(pre_history):len(the_history)]
        

        # first, thing to check is whether all of the calls are to cdo
        if len([f for f in the_history if f.startswith("cdo") == False]) > 0:
            raise ValueError("Not all of the calls are to cdo. Exiting!")
        
        # we need the start point.
        # this can be either a file or an ensemble
        # the end point is irrelevant
        
        # First remove anything with a comma
        start_point = [f for f in the_history[0].split(" ") if "," not in f]
        start_point = [f for f in start_point if f.endswith(".nc")][0:-1]
        start_point = " ".join(start_point)
        
        # we need to reverse the history so that the commands are in the correct order for chaining
        the_history.reverse()

        # now, pull all of the history together into one string
        # We can then tweak that
        
        the_history = "  ".join(the_history)
        # First, get rid of any mention of cdo
        the_history = the_history.replace("cdo ", "").replace("  ", " ")
        the_history = the_history.split(" ")
        # Now, we need to remove any files
        
        the_history = [f for f in the_history if ("," not in f and f.endswith(".nc")) == False]
        the_history = " ".join(the_history)
        the_history = " " + the_history
        # now, the cdo methods need to have a - in front of them
        
        for mm in cdo_methods:
            old_history = the_history
            the_history = the_history.replace(" " + mm, " -"+mm)
        
        temp_nc = tempfile.NamedTemporaryFile().name + ".nc"
        nc_created.append(temp_nc)
        run_this = "cdo " + the_history + " " +  start_point + " " + temp_nc
        run_this = run_this.replace("  ", " ")

        # OK. We might have reduced dimensions at one point. This needs to be handled.
        if "--reduce_dim" in run_this:
            run_this = run_this.replace("--reduce_dim", "")
            run_this = run_this.replace("cdo","cdo --reduce_dim")

        run_this = run_this.replace("cdo","cdo -L ")
        run_this = run_this.replace("  ", " ")
        run_command(run_this, self, silent)
        # Now we need to modify the history
        self.history = copy.deepcopy(self.hold_history)
        self.history.append(run_this)
        self.current = temp_nc



    return self
    
    
