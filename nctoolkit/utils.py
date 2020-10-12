
import subprocess

import xarray as xr
import pandas as pd
import netCDF4
import logging



def is_curvilinear(ff):
    """Function to work out if a file contains a curvilinear grid"""
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




