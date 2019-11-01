
from ._runthis import run_this

def monstat(self,  stat = "mean",  cores = 1):
    """Method to calculate the monthly statistic from a netcdf file""" 
    cdo_command = "cdo -mon" + stat

    run_this(cdo_command, self,  output = "ensemble", cores = cores)



def monthly_mean(self, cores = 1):

    """
    Calculate the monthly mean for each year/month combination in files. This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return monstat(self, stat = "mean", cores = cores)

def monthly_min(self, cores = 1):
    """
    Calculate the monthly minimums for each year/month combination in files. This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return monstat(self, stat = "min", cores = cores)

def monthly_max(self, cores = 1):
    """
    Calculate the monthly maximum for each year/month combination in files. This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return monstat(self, stat = "max",  cores = cores)
    
def monthly_range(self, cores = 1):

    """
    Calculate the monthly range for each year/month combination in files. This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return monstat(self, stat = "range", cores = cores)

