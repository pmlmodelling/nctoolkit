
from ._cleanup import cleanup 
from .flatten import str_flatten 
from ._runthis import run_this

def cdo_command(self, command, silent = True, cores = 1):
    """Method to call any cdo command of the the form 'command + infile + outfile'"""

    cdo_command = "cdo " + command

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)
