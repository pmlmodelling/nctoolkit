
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

    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    
    cdo_command = "cdo select,season=" + season + " " + self.current + " " + self.target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = self.target 
    
    cleanup(keep = self.current)
    
    return(self)



def select_months(self, months, silent = True):
    """Function to select months"""

    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    if type(months) is not list:
        months = [months]
    
    months = str_flatten(months, ",") 

    cdo_command = "cdo selmonth," + months + " " + self.current + " " + self.target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = self.target 
    
    cleanup(keep = self.current)
    
    return(self)


def select_years(self, years, silent = True):
    """Function to select years"""

    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    if type(years) is not list:
        years = [years]
    
    years = str_flatten(years, ",") 

    cdo_command = "cdo selyear," + years + " " + self.current + " " + self.target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = self.target 
    
    cleanup(keep = self.current)
    
    return(self)









