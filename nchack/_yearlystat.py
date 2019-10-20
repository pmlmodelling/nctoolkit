from ._cleanup import cleanup
from ._runthis import run_this

def yearlystat(self, stat = "mean", silent = True, cores = 1):
    """Function to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -year" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    

def yearly_mean(self, silent = True, cores = 1):
    """
    Calculate the yearly mean 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the yearly mean
    """
    return yearlystat(self, stat = "mean", silent = True, cores = cores)

def yearly_min(self, silent = True, cores = 1):
    """
    Calculate the yearly minimum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the yearly minimum
    """
    return yearlystat(self, stat = "min", silent = True, cores = cores)

def yearly_max(self, silent = True, cores = 1):
    """
    Calculate the yearly maximum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the yearly maximum
    """
    return yearlystat(self, stat = "max", silent = True, cores = cores)
    
def yearly_range(self, silent = True, cores = 1):
    """
    Calculate the yearly range 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the yearly range
    """
    return yearlystat(self, stat = "range", silent = True, cores = cores)
