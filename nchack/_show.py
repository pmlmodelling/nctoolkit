
import os
import tempfile

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def show_years(self):
    cdo_result = os.popen( "cdo showyear " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [int(v) for v in cdo_result]
    cdo_result.sort()
    return(cdo_result)


def show_months(self):
    cdo_result = os.popen( "cdo showmon " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    cdo_result = [int(v) for v in cdo_result]
    cdo_result.sort()
    return(cdo_result)

def show_levels(self):
    cdo_result = os.popen( "cdo showlevel " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    cdo_result = [int(v) for v in cdo_result]
    cdo_result.sort()
    return(cdo_result)


