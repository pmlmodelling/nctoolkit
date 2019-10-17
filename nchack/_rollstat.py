
from ._cleanup import cleanup
from ._runthis import run_this

def rollstat(self, window,  stat = "mean", silent = True, cores = 1):
    """Method to calculate the monthly statistic from a netcdf file""" 
    if type(window) is float:
        window = int(window)
        
    if type(window) is not int:
        raise ValueError("The window supplied is not numeric!")
    
    cdo_command = "cdo -run" + stat + "," + str(window)

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    

def rolling_mean(self, window, silent = True, cores = 1):

    """
    Calculate a rolling mean based on a window. 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling mean
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the rolling mean 
    """

    return rollstat(self, window = window, stat = "mean", silent = silent, cores = cores)

def rolling_min(self, window, silent = True, cores = 1):
    """
    Calculate a rolling minimum based on a window. 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling minimum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the rolling minimum 
    """

    return rollstat(self, window = window, stat = "min", silent = silent, cores = cores)

def rolling_max(self, window, silent = True, cores = 1):
    """
    Calculate a rolling maximum based on a window. 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling maximum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the rolling maximum 
    """
    return rollstat(self, window = window, stat = "max", silent = silent, cores = cores)
    
def rolling_range(self, window, silent = True, cores = 1):
    """
    Calculate a rolling range based on a window. 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling range
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the rolling range 
    """
    return rollstat(self, window = window, stat = "range", silent = silent, cores = cores)

def rolling_sum(self, window, silent = True, cores = 1):
    """
    Calculate a rolling sum based on a window. 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the rolling sum 
    """
    return rollstat(self, window = window, stat = "sum", silent = silent, cores = cores)

