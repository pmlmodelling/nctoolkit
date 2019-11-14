
import subprocess
from .flatten import str_flatten
from ._runthis import run_this

def cdo_command(self, command):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This must be of the form cdo command infile outfile, where cdo, infile and outfile are attached later.

    Returns
    -------------
    nchack.DataSet
        Original data set with cdo command applied.
    """

    # First carry out some checks

    if type(command) is not str:
        raise ValueError("Command supplied is not a str")

    read = subprocess.run("cdo --operators", shell = True, capture_output = True)
    cdo_methods = [x.split(" ")[0].replace("b'", "") for x in str(read.stdout).split("\\n")]

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

    if command.startswith("cdo "):
        command = command.replace("cdo ", " ")

    cdo_command = "cdo " + command + " "

    if "merge " in command or "mergetime " in command:
        output = "one"

    for mm in cdo_methods:
        if " " + mm + " " in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + " ", " -" + mm + " ")

        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ","," -" + mm + ",")

    run_this(cdo_command, self, output = "ensemble")

