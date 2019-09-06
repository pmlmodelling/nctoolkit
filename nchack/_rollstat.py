
from ._cleanup import cleanup
from ._runthis import run_this

def rollstat(self, window,  stat = "mean", silent = True, cores = 1):
    """Function to calculate the monthly statistic from a netcdf file""" 
    if type(window) is float:
        window = int(window)
        
    if type(window) is not int:
        raise ValueError("The window supplied is not numeric!")
    
    cdo_command = "cdo -run" + stat + "," + str(window)

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def rolling_mean(self, window, silent = True, cores = 1):
    return rollstat(self, window = window, stat = "mean", silent = silent, cores = cores)

def rolling_min(self, window, silent = True, cores = 1):
    return rollstat(self, window = window, stat = "min", silent = silent, cores = cores)

def rolling_max(self, window, silent = True, cores = 1):
    return rollstat(self, window = window, stat = "max", silent = silent, cores = cores)
    
def rolling_range(self, window, silent = True, cores = 1):
    return rollstat(self, window = window, stat = "range", silent = silent, cores = cores)

def rolling_sum(self, window, silent = True, cores = 1):
    return rollstat(self, window = window, stat = "sum", silent = silent, cores = cores)

