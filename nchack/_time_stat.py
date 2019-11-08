from ._runthis import run_this
from ._runthis import run_cdo
from ._session import nc_safe
from ._temp_file import temp_file
import os

def time_stat(self, stat = "mean", cores = 1):
    """Method to calculate a stat over all time steps"""
    cdo_command = "cdo -tim" + stat
    run_this(cdo_command, self,  output = "ensemble", cores = cores)
    
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



def percentile(self, p = 50, cores = 1):

    """
    Calculate the percentile of all values 

    Parameters
    -------------
    p: float or int
        Percentile to calculate 

    """
    if self.run == False:
        self.release()

    if type(p) not in [int, float]:
         raise ValueError("p is a " + str(type(p)) +  ", not int or float")


    target = temp_file("nc")

    cdo_command = "cdo -L -timpctl," + str(p) + " " + self.current + " -timmin " + self.current + " -timmax " + self.current + " "  + target

    target = run_cdo(cdo_command, target)

    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target

    nc_safe.append(target)






