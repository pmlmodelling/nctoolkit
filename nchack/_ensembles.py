import os
from ._temp_file import temp_file
from ._cleanup import cleanup
from ._runthis import run_this
from ._runthis import run_nco
from .flatten import str_flatten
from ._filetracker import nc_created
from ._filetracker import nc_safe


# Ensemble methods all assume the structure of the input files are idential
# So the time steps should be the same
# e.g. it could be an ensemble of climate models with the same variables and same times
# or it could be daily files for an entire year and you want the annual mean etc.
# Is there a way to check the ensemble without it being slow?



def ensemble_percentile(self, p = 50):
    """
    Calculate an ensemble percentile

    Parameters
    -------------
    p : float or int 
        percentile to calculate

    """

    if self.merged:
        raise ValueError("There is no point running this on a merged dataset. Check chains")

    # Throw an error if there is only a single file in the tracker
    if type(self.current) is not list:
        raise ValueError("The current state of the dataset is not a list")

    # This method cannot possibly be chained. Release it
    if self.run == False:
        self.release()

    cdo_command = "cdo -enspctl," + str(p)

    run_this(cdo_command, self, output = "one")

    # clean up the directory
    cleanup(keep = self.current)
    self.merged = True



def ensemble_nco(self, method, vars = None, ignore_time = False):
    """Method to calculate an ensemble stat from a list of files"""
    if self.merged:
        raise ValueError("There is no point running this on a merged dataset. Check chains")

    ff_ensemble = self.current

    # Throw an error if there is only a single file in the tracker
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the dataset is not a list")

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
    
    if ignore_time == False:
        if vars is None:
            nco_command = ("ncea -y " + method + " " + str_flatten(ff_ensemble, " ") + " " + target) 
        else:
            nco_command = ("ncea -y " + method + " -v " + str_flatten(vars, ",") + " " + str_flatten(ff_ensemble, " ") + " " + target) 
    else:
        if vars is None:
            nco_command = ("ncra -y " + method + " " + str_flatten(ff_ensemble, " ") + " " + target) 
        else:
            nco_command = ("ncra -y " + method + " -v " + str_flatten(vars, ",") + " " + str_flatten(ff_ensemble, " ") + " " + target) 

    target = run_nco(nco_command, target) 

    self.history.append(nco_command)

    if self.run:
        self.current = target 


    # remove the original files from the safe list
    for ff in ff_ensemble:
        nc_safe.remove(ff)

    # clean up the directory
    cleanup(keep = self.current)

    

def ensemble_min(self, vars = None, ignore_time = False):
    """
    Calculate an ensemble minimum

    Parameters
    -------------
    vars : str or list
        variables to analyse. If this is not supplied all variables will be analysed.
    ignore_time : boolean
        If True time is ignored when the statistic is ignored. If False, the statistics is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.

    """

    return ensemble_nco(self, "min", ignore_time = ignore_time, vars = vars)

def ensemble_max(self, vars = None, ignore_time = False):
    """
    Calculate an ensemble maximum

    Parameters
    -------------
    vars : str or list
        variables to analyse. If this is not supplied all variables will be analysed.
    ignore_time : boolean
        If True time is ignored when the statistic is ignored. If False, the statistics is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.

    """

    return ensemble_nco(self, "max", ignore_time = ignore_time, vars = vars)

def ensemble_mean(self, vars = None, ignore_time = False):
    """
    Calculate an ensemble mean

    Parameters
    -------------
    vars : str or list
        variables to analyse. If this is not supplied all variables will be analysed.
    ignore_time : boolean
        If True time is ignored when the statistic is ignored. If False, the statistics is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.

    """

    return ensemble_nco(self, "mean", ignore_time = ignore_time, vars = vars)



def ensemble_range(self):
    """
    Calculate an ensemble range

    Parameters
    -------------
    vars : str or list
        variables to analyse. If this is not supplied all variables will be analysed.
    ignore_time : boolean
        If True time is ignored when the statistic is ignored. If False, the statistics is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.

    """
    if type(self.current) is not list:
        raise ValueError("The current state of the dataset is not a list")

    cdo_command = "cdo ensrange " 

    run_this(cdo_command, self)

    # clean up the directory
    cleanup(keep = self.current)
    self.merged = True

def ensemble_mean_cdo(self,  vars = None):
    """
    Calculate an ensemble mean

    Parameters
    -------------
    vars : str or list
        variables to analyse. If this is not supplied all variables will be analysed.
    ignore_time : boolean
        If True time is ignored when the statistic is ignored. If False, the statistics is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.

    """

    if self.merged:
        raise ValueError("There is no point running this on a merged dataset. Check chains")

    ff_ensemble = self.current

    # Throw an error if there is only a single file in the tracker
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the dataset is not a list")

    ff_ensemble = self.current

    if vars is not None:
        if type(vars) == str:
            vars = [vars]

        if type(vars) is not list:
            raise ValueError("vars supplied is not a list or str!")

    
    cdo_command = "cdo -ensmean "
    self.history.append(cdo_command)


    if self.run:
        run_this(cdo_command, self, output = "one")
    else:
        self.release(run_merge = False)


    # clean up the directory
    cleanup(keep = self.current)
    self.merged = True


