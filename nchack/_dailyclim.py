from ._cleanup import cleanup
from ._runthis import run_this

def ydaystat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate daily climatologies""" 

    cdo_command = "cdo -yday" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)


def daily_mean_climatology(self, silent = True, cores = 1):
    return ydaystat(self, stat = "mean", silent = True, cores = cores)

def daily_min_climatology(self, silent = True, cores = 1):
    return ydaystat(self, stat = "min", silent = True, cores = cores)

def daily_max_climatology(self, silent = True, cores = 1):
    return ydaystat(self,  stat = "max", silent = True, cores = cores)
    
def daily_range_climatology(self, silent = True, cores = 1):
    return ydaystat(self, stat = "range", silent = True, cores = cores)

