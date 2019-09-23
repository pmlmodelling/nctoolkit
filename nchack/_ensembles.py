import os
import tempfile
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

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo enspctl," + str(p)

    run_this(cdo_command, self, silent, output = "one")

    # clean up the directory
    cleanup(keep = self.current)



def ensemble_nco(self, method, vars = None, silent = True):
    """Method to calculate an ensemble stat from a list of files"""
    if self.release == False:
        raise ValueError("NCO methods cannot be held over")

    ff_ensemble = self.current

    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")

    if vars is not None:
        if type(vars) == str:
            vars = [vars]

        if type(vars) is not list:
            raise ValueError("vars supplied is not a list or str!")

    target = tempfile.NamedTemporaryFile().name + ".nc"
    target = target.replace("tmp/", "tmp/nchack")

    global nc_created
    nc_created.append(target)
    
    if vars is None:
        nco_command = ("ncea -y " + method + " " + str_flatten(ff_ensemble, " ") + " " + target) 
    else:
        nco_command = ("ncea -y " + method + " -v " + str_flatten(vars, ",") + " " + str_flatten(ff_ensemble, " ") + " " + target) 

    self.history.append(nco_command)
    run_command(nco_command, self, silent) 
    if self.run: self.current = target 

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



def ensemble_check(self):
    "A function to check an ensemble is valid"

    results = []
    for ff in self.current:
        cdo_result = os.popen( "cdo partab " + ff).read()
        results.append(cdo_result)

    if len(list(set(results))) == 1:
        parameters = True
    else:
        parameters = False 
    if parameters == False:
        print("the same parameters are not available in all files")

    results = []

    for ff in self.current:
        cdo_result = os.popen( "cdo griddes " + ff).read()
        results.append(cdo_result)

    if len(list(set(results))) == 1:
        grid = True
    else:
        grid = False 

    if grid == False:
        print("the same grid is not available in all files")


