
import xarray as xr
import glob
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

# function to find files in directory with a specified variable 

def create_ensemble(path = "", var = None, recursive = True):
    "A function to create an ensemble is valid"
    # First make sure the path ends with "/" if it is not empty

    if path != "":
        if path.endswith("/") == False:
            path = path + "/"


    if recursive:   
        files = [f for f in glob.glob(path + "**/*.nc", recursive=True)]
    else:
        files = [f for f in glob.glob(path + "*.nc", recursive=True)]
    
    if var is None:
        ensemble = files
    else: 
        ensemble = []
        for ff in files:
            cdo_result = os.popen( "cdo showname " + ff).read()
            cdo_result = cdo_result.replace("\n", "").strip().split(" ")
            if var in cdo_result:
                ensemble.append(ff)
        

    return ensemble



