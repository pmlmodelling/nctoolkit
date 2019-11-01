from ._runthis import run_this

def ymonstat(self, stat = "mean",  cores = 1):
    """Method to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -ymon" + stat

    run_this(cdo_command, self,  output = "ensemble", cores = cores)



def monthly_mean_climatology(self, cores = 1):
    """
    Calculate the monthly mean climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return ymonstat(self, stat = "mean", cores = cores)

def monthly_min_climatology(self, cores = 1):
    """
    Calculate the monthly minimum climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return ymonstat(self, stat = "min", cores = cores)

def monthly_max_climatology(self, cores = 1):
    """
    Calculate the monthly maximum climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return ymonstat(self,  stat = "max",  cores = cores)
    
def monthly_range_climatology(self,  cores = 1):
    """
    Calculate the monthly range climatologies.  This applies to each file in an ensemble.

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """
    return ymonstat(self, stat = "range",  cores = cores)
