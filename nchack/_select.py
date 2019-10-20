
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def select_season(self, season, silent = True, cores = 1):
    """
    Select season from tracker

    Parameters
    -------------
    season : str
        Season to select. TBC.....
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the season selected
    """

    cdo_command = "cdo -select,season=" + season
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)

def select_months(self, months, silent = True, cores = 1):
    """
    Select months from tracker

    Parameters
    -------------
    months : list or int
        Month(s) to select. 
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the months selected
    """

    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    months = [int(x) for x in months]

    for x in months:
        if x not in list(range(1, 13)):
            raise ValueError("Months supplied are not valid!")

    months = str_flatten(months, ",") 

    cdo_command = "cdo -selmonth," + months + " "
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    

def select_years(self, years, silent = True, cores = 1):
    """
    Select years from tracker

    Parameters
    -------------
    months : list or int
        Month(s) to select. 
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the years selected
    """

    if type(years) is not list:
        years = [years]
    
    # convert years to int
    years = [int(x) for x in years]

    years = str_flatten(years, ",") 

    cdo_command = "cdo -selyear," + years
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    

def select_variables(self, vars = None, silent = True, cores = 1):
    """
    Select variables from tracker

    Parameters
    -------------
    months : list or int
        Month(s) to select. 
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the variables selected
    """


    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo -selname," + vars_list

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
def select_timestep(self, times, silent = True, cores = 1):
    """
    This method should probably be removed
    
    """

    if type(times) is not list:
        times = [times]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = "cdo -seltimestep," + times 

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)



