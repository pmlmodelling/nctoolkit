
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def select_season(self, season, silent = True, cores = 1):
    """Method to select the season"""

    cdo_command = "cdo select,season=" + season
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)

def select_months(self, months, silent = True, cores = 1):
    """Method to select months"""

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
    

def select_years(self, years, silent = True, cores = 1):
    """Method to select years"""

    if type(years) is not list:
        years = [years]
    
    # convert years to int
    years = [int(x) for x in years]

    years = str_flatten(years, ",") 

    cdo_command = "cdo selyear," + years
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    

def select_variables(self, vars = None, silent = True, cores = 1):
    """Method to select variables from a netcdf file"""

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo selname," + vars_list

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
def select_timestep(self, times, silent = True, cores = 1):
    """Method to select time steps"""

    if type(times) is not list:
        times = [times]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = "cdo seltimestep," + times 

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)



