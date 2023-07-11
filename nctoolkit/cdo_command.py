import subprocess
import os

from nctoolkit.runthis import run_this


def cdo_command(self, command=None, ensemble=False):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This command must be such that
        "cdo {command} infile outfile" will run.
    ensemble : bool
        Is this an ensemble command?
    """

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if not isinstance(command, str):
        raise TypeError("Command supplied is not a str")

    if command.startswith("cdo "):
        command = command.replace("cdo ", " ").strip()
    read = subprocess.run(
        "cdo --operators", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout

    cdo_methods = [x.split(" ")[0].replace("b'", "") for x in str(read).split("\\n")]

    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

    cdo_methods.append("L")
    cdo_methods.append("reduce_dim")

    for x in command.replace("-f ", "").replace("-z ", "").strip().split(" "):
        y = x.split(",")[0].replace("-", "")
        if y not in cdo_methods and y != "nc4" and y != "zip_9":
            if not os.path.exists(y):
                raise ValueError(f"{y} is not a cdo method!" + y)

    new_command = ""
    for cc in command.split(" "):
        if cc in cdo_methods:
            new_command += " -" + cc
        else:
            new_command += " " + cc

    new_command = new_command.strip()
    new_command = new_command.replace("  ", " ")

    # remove cdo from the command

    output = "ensemble"
    cdo_command = "cdo " + new_command + " "

    if ("merge " in cdo_command) or ("mergetime " in cdo_command) or ensemble:
        output = "one"
        self._merged = True

    for mm in cdo_methods:
        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ",", " -" + mm + ",")
    cdo_command = cdo_command.strip()

    run_this(cdo_command, self, output=output)
