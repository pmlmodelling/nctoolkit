import subprocess
import os

from nctoolkit.runthis import run_this
from nctoolkit.session import session_info


def cdo_command(self, command=None, ensemble=False, check=False):
    """
    cdo_command: Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This command must be such that
        "cdo {command} infile outfile" will run.
    ensemble : bool
        Is this an ensemble method command? For example ensmean, mergetime, etc.
    check : bool
        Check whether the command is valid

    Examples
    -------------
    Use CDO to select a year from a dataset
    >>> ds.cdo_command("selyear,2000")

    """

    # First, check that the command is valid
    if command is None:
        raise ValueError("Please supply a command")

    if not isinstance(command, str):
        raise TypeError("Command supplied is not a str")

    if command.startswith("cdo "):
        command = command.replace("cdo ", " ").strip()

    if check:
        read = subprocess.run(
            "cdo --operators",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

        cdo_methods = [
            x.split(" ")[0].replace("b'", "") for x in str(read).split("\\n")
        ]

        cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

        cdo_methods.append("L")
        cdo_methods.append("reduce_dim")

        # test whether the command is a valid CDO command
        test_command = command

        # remove anything within quotes from test_command

        while '"' in test_command:
            test_command = test_command.replace(
                test_command[test_command.find('"') : test_command.find('"', 1) + 1], ""
            )

        while "'" in test_command:
            test_command = test_command.replace(
                test_command[test_command.find("'") : test_command.find("'", 1) + 1], ""
            )

        test_command = test_command.replace("  ", " ")

        for x in test_command.replace("-f ", "").replace("-z ", "").strip().split(" "):
            y = x.split(",")[0].replace("-", "")
            if y not in cdo_methods and y != "nc4" and y != "zip_9":
                if not os.path.exists(y):
                    raise ValueError(f"{y} is not a cdo method!" + y)

    new_command = ""
    for cc in command.split(" "):
        if cc in session_info["cdo_methods"]:
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

    for mm in session_info["cdo_methods"]:
        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ",", " -" + mm + ",")
    cdo_command = cdo_command.strip()

    run_this(cdo_command, self, output=output)
