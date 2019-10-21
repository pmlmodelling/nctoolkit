from ._cleanup import cleanup
from ._runthis import run_this

def ydaystat(self, stat = "mean", cores = 1):
    """Method to calculate daily climatologies""" 

    cdo_command = "cdo -yday" + stat

    run_this(cdo_command, self, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)


def daily_mean_climatology(self, cores = 1):
    """
    Calculate a daily mean climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the daily climatology
    """

    return ydaystat(self, stat = "mean", cores = cores)

def daily_min_climatology(self, cores = 1):
    """
    Calculate a daily minimum climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the daily climatology
    """

    return ydaystat(self, stat = "min", cores = cores)

def daily_max_climatology(self, cores = 1):
    """
    Calculate a daily maximum climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the daily climatology
    """
    return ydaystat(self,  stat = "max", cores = cores)
    
def daily_range_climatology(self, cores = 1):
    """
    Calculate a daily range climatology. This assumes times in files are directly comparable, so make sure the same number of days are in each file

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the daily climatology
    """
    return ydaystat(self, stat = "range", cores = cores)

