from ._cleanup import cleanup
from ._runthis import run_this

def ymonstat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -ymon" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)


def monthly_mean_climatology(self, silent = True, cores = 1):
    """
    Calculate the monthly mean climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with monthly climatologies
    """
    return ymonstat(self, stat = "mean", silent = True, cores = cores)

def monthly_min_climatology(self, silent = True, cores = 1):
    """
    Calculate the monthly minimum climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with monthly climatologies
    """
    return ymonstat(self, stat = "min", silent = True, cores = cores)

def monthly_max_climatology(self, silent = True, cores = 1):
    """
    Calculate the monthly maximum climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with monthly climatologies
    """
    return ymonstat(self,  stat = "max", silent = True, cores = cores)
    
def monthly_range_climatology(self, silent = True, cores = 1):
    """
    Calculate the monthly range climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with monthly climatologies
    """
    return ymonstat(self, stat = "range", silent = True, cores = cores)
