
import os
import tempfile

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runthis import run_this


def select_season(self, season, silent = True, cores = 1):
    """Function to select the season"""

    cdo_command = "cdo select,season=" + season
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    return(self)



def select_months(self, months, silent = True, cores = 1):
    """Function to select months"""

    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    months = [int(x) for x in months]

    for x in months:
        if x not in list(range(1, 13)):
            raise ValueError("Months supplied are not valid!")

    months = str_flatten(months, ",") 

    cdo_command = "cdo selmonth," + months + " "
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    return(self)


def select_years(self, years, silent = True, cores = 1):
    """Function to select years"""

    if type(years) is not list:
        years = [years]
    
    # convert years to int
    years = [int(x) for x in years]

    years = str_flatten(years, ",") 

    cdo_command = "cdo selyear," + years + " " + self.current + " " + target
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    return(self)









