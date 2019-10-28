import os

from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def select_season(self, season,  cores = 1):
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
    nchack.DataSet
        Reduced tracker with the season selected
    """

    cdo_command = "cdo -select,season=" + season
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)

def select_months(self, months,  cores = 1):
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
    nchack.DataSet
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
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    

def select_years(self, years,  cores = 1):
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
    nchack.DataSet
        Reduced tracker with the years selected
    """

    if type(years) is not list:
        years = [years]
    
    # convert years to int
    years = [int(x) for x in years]


    if type(self.current) is list:
        new_current = []
        for ff in self.current:
            cdo_result = os.popen( "cdo showyear " + ff).read()
            cdo_result = cdo_result.replace("\n", "")
            cdo_result = cdo_result.split()
            cdo_result = list(set(cdo_result))
            cdo_result =  [int(v) for v in cdo_result]
            inter = [element for element in cdo_result if element in years]
            if len(inter) > 0:
                new_current.append(ff)
            if len(inter) == 0:
                print("Warning: " + ff + " has none of the years, so has been removed!")
        if len(new_current) == 0:
            raise ValueError("Data for none of the years is available!")

        self.current = new_current
        
    years = str_flatten(years, ",") 

    cdo_command = "cdo -selyear," + years
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    

def select_variables(self, vars = None,  cores = 1):
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
    nchack.DataSet
        Reduced tracker with the variables selected
    """


    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo -selname," + vars_list

    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
def select_timestep(self, times,  cores = 1):
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

    run_this(cdo_command, self,  output = "ensemble", cores = cores)



