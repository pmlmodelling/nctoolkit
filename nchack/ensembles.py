import os
import copy
from .temp_file import temp_file
from .runthis import run_this
from .runthis import run_nco
from .flatten import str_flatten
from .session import nc_safe
from .cleanup import cleanup
import warnings

def ensemble_percentile(self, p = 50):
    """
    Calculate an ensemble percentile
    This will calculate the percentles for each time step in the files. For example, if you had an ensemble of files where each file included 12 months of data, it would calculate the percentile for each month.

    Parameters
    -------------
    p : float or int
        percentile to calculate
    """

    # This method cannot possibly be chained. Release it
    self.release()

    # Throw an error if there is only a single file in the tracker
    if type(self.current) is not list:
        warnings.warn(message = "There is only one file in the dataset")

    if type(p) not in [int, float]:
        raise TypeError("p is a " + str(type(p)) + ", not an int or float")

    cdo_command = "cdo -enspctl," + str(p) + " "

    run_this(cdo_command, self, output = "one")

    # clean up the directory
    self._merged = True



def ensemble_nco(self, method, vars = None, ignore_time = False):
    """
    NCO Method to calculate an ensemble stat from a list of files
    """

    # This method cannot possibly be chained. Release it
    self.release()

    ff_ensemble = copy.deepcopy(self.current)

    # Throw an error if there is only a single file in the tracker
    if type(ff_ensemble) is not list:
        warnings.warn("There is only one file in the dataset")

    ff_ensemble = self.current

    if vars is not None:
        if type(vars) == str:
            vars = [vars]

        if type(vars) is not list:
            raise TypeError("vars supplied is not a list or str!")

    # generate a temp files
    target = temp_file("nc")

    # generate the nco call
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

    # run the call
    target = run_nco(nco_command, target)

    #add the call to the history and tempfile to nc_safe
    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)

    self.current = target
    nc_safe.append(self.current)

    # remove the original files from the safe list
    for ff in ff_ensemble:
        if ff in nc_safe:
            nc_safe.remove(ff)

    cleanup()


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
        raise TypeError("The current state of the dataset is not a list")

    self.release()

    cdo_command = "cdo ensrange "

    run_this(cdo_command, self)

    self._merged = True


