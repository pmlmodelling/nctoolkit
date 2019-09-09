
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this
from ._variables import variables
from ._variables import nc_variables


def select_season(self, season, silent = True, cores = 1):
    """Method to select the season"""

    cdo_command = "cdo select,season=" + season
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    #return self


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
    
    ##return self


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
    
    #return self


def select_variables(self, vars = None, silent = True, cores = 1):
    """Method to select variables from a netcdf file"""

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    
    if type(self.current) is str:
        file_list = [self.current]
    else:
        file_list = self.current

    for ff in file_list:    
        valid_vars = nc_variables(ff)
        for vv in vars_list:
            if vv not in valid_vars:
                raise ValueError(vv + " is not available in " + ff)

    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo selname," + vars_list

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
  #  return self
