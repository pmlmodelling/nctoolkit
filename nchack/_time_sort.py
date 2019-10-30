from ._runthis import run_this
from .flatten import str_flatten
from ._cleanup import cleanup

def sort_times(self, cores = 1):
    """
    Sort by time 

    """

    cdo_command = ("cdo -timsort," + lat_box)
    run_this(cdo_command, self, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)
