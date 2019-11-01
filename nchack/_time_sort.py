from ._runthis import run_this
from .flatten import str_flatten

def sort_times(self, cores = 1):
    """
    Sort by time 

    """

    cdo_command = "cdo -sorttimestamp"
    run_this(cdo_command, self, output = "ensemble", cores = cores)

