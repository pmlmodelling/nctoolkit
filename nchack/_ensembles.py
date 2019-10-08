import os
from ._temp_file import temp_file
from ._cleanup import cleanup
from ._runthis import run_this
from .flatten import str_flatten
from ._filetracker import nc_created
from ._runcommand import run_command


# Ensemble methods all assume the structure of the input files are idential
# So the time steps should be the same
# e.g. it could be an ensemble of climate models with the same variables and same times
# or it could be daily files for an entire year and you want the annual mean etc.
# Is there a way to check the ensemble without it being slow?



def ensemble_percentile(self, p = 50, silent = True):
    """Method to calculate an ensemble percentile from a list of files"""

    if self.merged:
        raise ValueError("There is no point running this on a merged tracker. Check chains")

    # Throw an error if there is only a single file in the tracker
    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    # This method cannot possibly be chained. Release it
    if self.run == False:
        self.release()

    cdo_command = "cdo enspctl," + str(p)

    run_this(cdo_command, self, silent, output = "one")

    # clean up the directory
    cleanup(keep = self.current)
    self.merged = True



def ensemble_nco(self, method, vars = None, silent = True):
    """Method to calculate an ensemble stat from a list of files"""
    if self.merged:
        raise ValueError("There is no point running this on a merged tracker. Check chains")
    # Throw an error if there is only a single file in the tracker
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")

    # This method cannot possibly be chained. Release it
    if self.run == False:
        self.release()

    ff_ensemble = self.current

    if vars is not None:
        if type(vars) == str:
            vars = [vars]

        if type(vars) is not list:
            raise ValueError("vars supplied is not a list or str!")

    target = temp_file("nc") 

    global nc_created
    nc_created.append(target)
    
    if vars is None:
        nco_command = ("ncea -y " + method + " " + str_flatten(ff_ensemble, " ") + " " + target) 
    else:
        nco_command = ("ncea -y " + method + " -v " + str_flatten(vars, ",") + " " + str_flatten(ff_ensemble, " ") + " " + target) 

    self.history.append(nco_command)
    run_command(nco_command, self, silent) 
    if self.run:
        self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

    

def ensemble_min(self, vars = None, silent = True):
    """Method to calculate an ensemble min from a list of files"""
    return ensemble_nco(self, "min", vars = vars)

def ensemble_max(self, vars = None, silent = True):
    """Method to calculate an ensemble max from a list of files"""
    return ensemble_nco(self, "max", vars = vars)

def ensemble_mean(self, vars = None, silent = True):
    """Method to calculate an ensemble mean from a list of files"""
    return ensemble_nco(self, "mean", vars = vars)



def ensemble_range(self, silent = True):
    """Method to calculate an ensemble range from a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo ensrange " 

    run_this(cdo_command, self, silent, output = "one")

    # clean up the directory
    cleanup(keep = self.current)
    self.merged = True

