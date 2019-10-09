from ._cleanup import cleanup
from ._runthis import run_this
from ._filetracker import nc_created
from ._temp_file import temp_file
import os

def time_stat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate a stat over all time steps"""
    cdo_command = "cdo -tim" + stat
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
    
def sum(self, silent = True, cores = 1):
    return time_stat(self, stat = "sum", silent = silent, cores = cores)

def mean(self, silent = True, cores = 1):
    return time_stat(self, stat = "mean", silent = silent, cores = cores)

def min(self, silent = True, cores = 1):
    return time_stat(self, stat = "min", silent = silent, cores = cores)

def max(self, silent = True, cores = 1):
    return time_stat(self, stat = "max", silent = silent, cores = cores)

def range(self, silent = True, cores = 1):
    return time_stat(self,stat = "range", silent = silent, cores = cores)

def var(self, silent = True, cores = 1):
    return time_stat(self, stat = "var", silent = silent, cores = cores)


def cum_sum(self, silent = True, cores = 1):
    """Method to calculate a stat over all time steps"""
    cdo_command = "cdo -timcumsum" 
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
    
def sum(self, silent = True, cores = 1):
    return time_stat(self, stat = "sum", silent = silent, cores = cores)



