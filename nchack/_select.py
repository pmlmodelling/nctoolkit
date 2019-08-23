
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command


def select_season(self, season, silent = True):
    """Function to select the season"""

    target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    
    cdo_command = "cdo select,season=" + season + " " + self.current + " " + target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = target 
    
    cleanup(keep = self.current)
    
    return(self)



def select_months(self, months, silent = True):
    """Function to select months"""

    target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    months = [int(x) for x in months]

    for x in months:
        if x not in list(range(1, 13)):
            raise ValueError("Months supplied are not valid!")

    months = str_flatten(months, ",") 

    cdo_command = "cdo selmonth," + months + " " + self.current + " " + target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = target 
    
    cleanup(keep = self.current)
    
    return(self)


def select_years(self, years, silent = True):
    """Function to select years"""

    target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    if type(years) is not list:
        years = [years]
    
    # convert years to int
    years = [int(x) for x in years]

    years = str_flatten(years, ",") 


    cdo_command = "cdo selyear," + years + " " + self.current + " " + target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = target 
    
    cleanup(keep = self.current)
    
    return(self)









