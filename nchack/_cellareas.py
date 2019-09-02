
import tempfile

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runthis import run_this

def cell_areas(self, silent = True):

    cdo_command = "cdo gridarea "
    run_this(cdo_command, self, silent, output = "ensemble")

    cleanup(keep = self.current)
    
    return(self)

