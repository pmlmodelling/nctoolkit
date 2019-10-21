
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def zip(self,  cores = 1):
    """
    Zip the tracker

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Zipped tracker
    """

    if self.run == True:
        cdo_command = "cdo -z zip copy "
    else:
        cdo_command = "cdo -z zip "
    run_this(cdo_command, self, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
