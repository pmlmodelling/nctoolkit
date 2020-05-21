
import subprocess

from nctoolkit.runthis import run_this


def cdo_command(self, command=None):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This command must be such that "cdo {command} infile outfile" will run.
    """

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if type(command) is not str:
        raise TypeError("Command supplied is not a str")

    if command.startswith("cdo "):
        command = command.replace("cdo ", " ").strip()
    read = subprocess.run(
        "cdo --operators", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout

    cdo_methods = [x.split(" ")[0].replace("b'", "") for x in str(read).split("\\n")]

    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

    n_methods = 0

    for x in command.split(" "):
        y = x.split(",")[0].replace("-", "")
        if y not in cdo_methods:
            raise ValueError("You have supplied an invalid cdo method:" + y)

    # remove cdo from the command

    output = "ensemble"
    cdo_command = "cdo " + command + " "

    if ("merge " in cdo_command) or ("mergetime " in cdo_command):
        output = "one"
        self._merged = True

    for mm in cdo_methods:

        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ",", " -" + mm + ",")

    run_this(cdo_command, self, output=output)
