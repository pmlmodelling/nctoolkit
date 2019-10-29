from ._cleanup import cleanup
from ._runthis import run_this
from ._filetracker import nc_created
from ._temp_file import temp_file
import os

def time_stat(self, stat = "mean", cores = 1):
    """Method to calculate a stat over all time steps"""
    cdo_command = "cdo -tim" + stat
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
    
def sum(self,  cores = 1):
    """
    Calculate the sum of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self, stat = "sum",  cores = cores)

def mean(self,  cores = 1):
    """
    Calculate the mean of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self, stat = "mean",  cores = cores)

def min(self,  cores = 1):
    """
    Calculate the minimums of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self, stat = "min",  cores = cores)

def max(self,  cores = 1):
    """
    Calculate the maximums of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self, stat = "max",  cores = cores)

def range(self,  cores = 1):
    """
    Calculate the ranges of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self,stat = "range",  cores = cores)

def var(self,  cores = 1):
    """
    Calculate the variances of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return time_stat(self, stat = "var",  cores = cores)


def cum_sum(self,  cores = 1):
    """
    Calculate the cumulative sums of all values.  

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    cdo_command = "cdo -timcumsum" 
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
