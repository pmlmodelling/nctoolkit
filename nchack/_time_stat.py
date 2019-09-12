from ._cleanup import cleanup
from ._runthis import run_this
from ._filetracker import nc_created
import tempfile
import os

def time_stat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate a stat over all time steps"""
    cdo_command = "cdo tim" + stat
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
    

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



#def percentile(self, p = 50, silent = True, cores = 1):
#    """Method to calculate the percentile over all time steps"""
#    if self.run == False:
#        raise ValueError("You cannot currently run percentile in hold mode")
#    minfile = tempfile.NamedTemporaryFile().name + ".nc"
#    nc_created.append(minfile)
#
#    os.system("cdo timmin " + self.current + " " + minfile)
#    if os.path.exists(minfile) == False:
#        raise ValueError("Calculating a time minimum was not successful. Check output")
#
#    maxfile = tempfile.NamedTemporaryFile().name + ".nc"
#    nc_created.append(maxfile)
#
#    os.system("cdo timmax " + self.current + " " + maxfile)
#
#    if os.path.exists(maxfile) == False:
#        raise ValueError("Calculating a time maximum was not successful. Check output")
#
#    cdo_command = "cdo timpctl," + str(p) + " " + minfile + " " + maxfile  
#    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    # clean up the directory
    cleanup(keep = self.current)
 



