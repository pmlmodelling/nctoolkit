import logging
import netCDF4
import pandas as pd
import re
import subprocess
import xarray as xr

def is_curvilinear(ff):
    """
    Function to work out if a file contains a curvilinear grid
    """
    cdo_result = subprocess.run(
        f"cdo sinfo {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return (
        len(
            [
                x
                for x in cdo_result.stdout.decode("utf-8").split("\n")
                if "curvilinear" in x
            ]
        )
        > 0
    )
def version_below(x,y):
    x = x.split(".")
    x = int(x[0])* 1000 +  int(x[1]) * 100+  int(x[2])
    
    y = y.split(".")
    y = int(y[0])* 1000 +  int(y[1]) * 100+  int(y[2])
    
    return x < y

def version_above(x,y):
    x = x.split(".")
    x = int(x[0])* 1000 +  int(x[1]) * 100+  int(x[2])
    
    y = y.split(".")
    y = int(y[0])* 1000 +  int(y[1]) * 100+  int(y[2])
    
    return x > y
# check version of cdo installed


def validate_version():
    """
    Function to tell the user whether a valid version of CDO is installed
    """
    bad = False

    try:
        version = cdo_version()
        bad = version_above(cdo_version(), "2.0.0")
        actual_version = version
        if version is None:
            print(
                "Please install CDO version 1.9.4 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
            )
        sub = "."
        wanted = ""
        n = 3
        where = [m.start() for m in re.finditer(sub, version)][n - 1]

        version = re.sub("[A-Za-z]", "", version)

        before = version[:where]
        after = version[where:]
        after = after.replace(sub, wanted)
        newString = before + after
        if float(newString) >= 1.94 == False:
            print(
                "Please install CDO version 1.9.4 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
            )
        else:
            print(f"nctoolkit is using Climate Data Operators version {actual_version}")
    except:
        print(
            "Please install CDO version 1.9.4 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
        )
    if bad: 
        raise ValueError("This version of nctoolkit is not compatible with CDO versions 2.0.0 and above")


def cdo_version():
    """
    Function to identify the CDO version
    """
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    version = [
        x
        for x in str(cdo_check.stderr).split("\n")
        if "version" in x and "cdo" in x
    ]
    if len(version) == 0:
        version = [
            x
            for x in str(cdo_check.stdout).split("\n")
            if "version" in x and "cdo" in x
        ]
        if len(version) == 0:
            return None
    version = version[0]

    candidates = [
        x for x in version.split(" ") if x.startswith("1") or x.startswith("2")
    ]
    return candidates[0]
