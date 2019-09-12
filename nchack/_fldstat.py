
from ._cleanup import cleanup
from ._runthis import run_this

def fldstat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate the spatial stat from a netcdf""" 

    cdo_command = "cdo -fld" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    ##return self
    

def spatial_mean(self, silent = True, cores = 1):
    return fldstat(self, stat = "mean", silent = True, cores = cores)

def spatial_min(self, silent = True, cores = 1):
    return fldstat(self, stat = "min", silent = True, cores = cores)

def spatial_max(self, silent = True, cores = 1):
    return fldstat(self, stat = "max", silent = True, cores = cores)
    
def spatial_range(self, silent = True, cores = 1):
    return fldstat(self, stat = "range", silent = True, cores = cores)
