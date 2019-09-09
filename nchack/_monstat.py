
from ._cleanup import cleanup
from ._runthis import run_this

def monstat(self,  stat = "mean", silent = True, cores = 1):
    """Method to calculate the monthly statistic from a netcdf file""" 
    cdo_command = "cdo -mon" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

#    return self
    

def monthly_mean(self, silent = True, cores = 1):
    return monstat(self, stat = "mean", silent = silent, cores = cores)

def monthly_min(self, silent = True, cores = 1):
    return monstat(self, stat = "min", silent = silent, cores = cores)

def monthly_max(self, silent = True, cores = 1):
    return monstat(self, stat = "max", silent = silent, cores = cores)
    
def monthly_range(self, silent = True, cores = 1):
    return monstat(self, stat = "range", silent = silent, cores = cores)

