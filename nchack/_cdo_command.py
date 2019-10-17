
from ._cleanup import cleanup 
from .flatten import str_flatten 
from ._runthis import run_this
import os

def cdo_command(self, command, silent = True, cores = 1):
    """
    Apply a cdo command to a tracker

    Parameters
    -------------
    command : string
        cdo command to call. This must be of the form cdo command infile outfile, where cdo, infile and outfile are attached later. 
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Original tracker with cdo command applied. 

    """


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

    cdo_command = "cdo " + command + " "

    if "merge " in command or "mergetime " in command:
        output = "one"

    for mm in cdo_methods:
        if " " + mm + " " in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + " ", " -" + mm + " ")

        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ","," -" + mm + ",")

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)
