
from ._cleanup import cleanup 
from .flatten import str_flatten 
from ._runthis import run_this
import os

def cdo_command(self, command, silent = True, cores = 1):
    """Method to call any cdo command of the the form 'command + infile + outfile'"""

    # First carry out some checks

    if type(command) is not str:
        raise ValueError("Command supplied is not a str")

    read = os.popen("cdo --operators").read()
    cdo_methods = [x.split(" ")[0] for x in read.split("\n")]
    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

    n_methods = 0

    for x in command.split(" "):
        for y in x.split(","):
            if y.replace("-", "") in cdo_methods:
                n_methods+=1

    if n_methods == 0:
        raise ValueError("You have not supplied any cdo methods!")

    if n_methods > 1:
        raise ValueError("Errror: please supply one cdo method")

    cdo_command = "cdo " + command

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)
