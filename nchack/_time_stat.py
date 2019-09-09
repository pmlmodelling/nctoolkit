from ._cleanup import cleanup
from ._runthis import run_this

def time_stat(self, stat = "mean", silent = True, cores = 1):
    """Function to calculate the mean from from a single file"""
    cdo_command = "cdo tim" + stat
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
    return self
    

def time_mean(self, silent = True, cores = 1):
    return time_stat(self, stat = "mean", silent = silent, cores = cores)

def time_min(self, silent = True, cores = 1):
    return time_stat(self, stat = "min", silent = silent, cores = cores)

def time_max(self, silent = True, cores = 1):
    return time_stat(self, stat = "max", silent = silent, cores = cores)

def time_range(self, silent = True, cores = 1):
    return time_stat(self,stat = "range", silent = silent, cores = cores)

def time_var(self, silent = True, cores = 1):
    return time_stat(self, stat = "var", silent = silent, cores = cores)





    
