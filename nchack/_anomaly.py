import os
import glob
import copy
from ._temp_file import temp_file
import multiprocessing

from ._filetracker import nc_created
from ._filetracker import nc_safe
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
from ._time_stat import mean
from ._rename import rename
from ._cdo_command import cdo_command 
from ._expr import transmute
from ._cleanup import cleanup
import copy


def anomaly_annual(self, var = None, base_years = None, silent = False):
    """
    Method to calculate annual anomalies based on a baseline period
    """

    if type(self.current) is not str:
        raise ValueError("Splitting the file by year did not work!")

    if type(var) is not str:
        raise ValueError("This method currently only works with single variables")

    if type(base_years) is not list:
        raise ValueError("baseline years supplied is not a list")

    # Calculate the yearly mean 
    new_tracker = copy.deepcopy(self)
    new_tracker.select_variables(var)
    new_tracker.rename({var:"observed"})
    new_tracker.yearly_mean()
    nc_safe.append(new_tracker.current)

    remove_later = copy.deepcopy(new_tracker.current)

    # calculate the climatology
    clim_tracker = copy.deepcopy(self)
    clim_tracker.select_variables(var)
    clim_tracker.select_years(base_years)
    clim_tracker.mean()
    clim_tracker.rename({var:"base"})
    nc_safe.append(copy.deepcopy(clim_tracker.current))
    
    target = temp_file("nc") 

    nc_created.append(target)
    nc_safe.append(target)
    os_command = "cdo -L -expr,'anomaly=observed-base' -merge " + new_tracker.current + " " + clim_tracker.current + " " + target

    new_tracker.history.append(os_command)

    new_tracker.current = target
    os.system(os_command)

    if os.path.exists(target) == False:
        raise ValueError("Calculating the anomaly failed")

    nc_safe.remove(clim_tracker.current)
    nc_safe.remove(remove_later)

    cleanup(keep = new_tracker.current)

    del clim_tracker

    nc_safe.remove(target)
    print(os.path.exists(target))

    return(new_tracker)
    
    









    




