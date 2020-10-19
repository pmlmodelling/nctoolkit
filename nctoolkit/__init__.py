from nctoolkit.api import (
    open_data,
    merge,
    cor_time,
    cor_space,
    options,
    DataSet,
    open_thredds,
    open_url,
)
from nctoolkit.cleanup import cleanup, clean_all, deep_clean, temp_check
from nctoolkit.create_ensemble import create_ensemble
from nctoolkit.session import show_session, session_files
from nctoolkit.show import nc_variables, nc_years

import re
import subprocess

# check version of cdo installed


def valid(string):
    sub = "."
    wanted = ""
    n = 3
    where = [m.start() for m in re.finditer(sub, string)][n - 1]

    string = re.sub("[A-Za-z]", "", string)

    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted)
    newString = before + after
    return float(newString) >= 1.93


cdo_check = subprocess.run(
    "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

cdo_error = False
if "error" in str(cdo_check.stderr):
    error_message = str(cdo_check.stderr).replace("\\n", "").replace("b'", "").replace("cdo:", "").strip()
    raise ValueError(f"Error loading CDO: {error_message}")

if cdo_error is False:

    cdo_check = str(cdo_check.stdout).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()


    if "error" in cdo_check:
         print(f"There is a problem with the CDO installation: {cdo_check}")

    if len(cdo_check) < 2:
        print(
            "Please install CDO version 1.9.3 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
        )
    else:
        cdo_check = subprocess.run(
            "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        cdo_check = str(cdo_check.stderr).replace("\\n", "")
        cdo_check = cdo_check.replace("b'", "").strip()
        cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]
        if valid(cdo_version) is False:
            print(
                "Please install CDO version 1.9.3 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
            )
