
from ._runthis import run_this

def fldstat(self, stat = "mean",  cores = 1):
    """Method to calculate the spatial stat from a netcdf""" 

    #cdo_command = "cdo --reduce_dim -fld" + stat
    cdo_command = "cdo -fld" + stat

    run_this(cdo_command, self,  output = "ensemble", cores = cores)

def spatial_mean(self, cores = 1):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return fldstat(self, stat = "mean", cores = cores)

def spatial_mean(self, cores = 1):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return fldstat(self, stat = "mean", cores = cores)

def spatial_min(self, cores = 1):
    """
    Calculate a spatial minimum of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return fldstat(self, stat = "min",  cores = cores)

def spatial_max(self, cores = 1):
    """
    Calculate a spatial maximum of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return fldstat(self, stat = "max", cores = cores)
    
def spatial_range(self, cores = 1):
    """
    Calculate a spatial range of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return fldstat(self, stat = "range",  cores = cores)

def spatial_sum(self, cores = 1):
    """
    Calculate the spatial sum of variables. This is performed for each time step.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return fldstat(self, stat = "sum", cores = cores)
