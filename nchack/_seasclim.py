
from ._cleanup import cleanup
from ._runthis import run_this

def seasstat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate the seasonal statistic from a function""" 
    cdo_command = "cdo -yseas" + stat 

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    

def seasonal_mean_climatology(self, silent = True, cores = 1):

    """
    Calculate a seasonal mean climatology 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the climatology 
    """

    return seasstat(self, stat = "mean", silent = True, cores = cores)

def seasonal_min_climatology(self, silent = True, cores = 1):
    """
    Calculate a seasonal minimum climatology 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the climatology 
    """
    return seasstat(self, stat = "min", silent = True, cores = cores)

def seasonal_max_climatology(self, silent = True, cores = 1):
    """
    Calculate a seasonal maximum climatology 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the climatology 
    """
    return seasstat(self, stat = "max", silent = True, cores = cores)
    
def seasonal_range_climatology(self, silent = True, cores = 1):
    """
    Calculate a seasonal range climatology 

    Parameters
    -------------
    window = int
        The size of the window for the calculation of the rolling sum
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the climatology 
    """
    return seasstat(self, stat = "range", silent = True, cores = cores)
