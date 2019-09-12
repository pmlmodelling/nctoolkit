from ._cleanup import cleanup
from ._runthis import run_this

def cell_areas(self, silent = True, cores = 1):
    cdo_command = "cdo gridarea "
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    cleanup(keep = self.current)
    #return self
