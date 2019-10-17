from ._cleanup import cleanup
from ._runthis import run_this

def cell_areas(self, silent = True, cores = 1):
    """
    Calculate the cell areas in square meters

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with cell areas 

    """

    cdo_command = "cdo -gridarea "
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    cleanup(keep = self.current)
