
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

# function to get list of variables

def ensemble_check(self):
    "A function to check an ensemble is valid"

    results = []
    for ff in self.current:
        cdo_result = os.popen( "cdo partab " + ff).read()
        results.append(cdo_result)

    if len(list(set(results))) == 1:
        parameters = True
    else:
        parameters = False 
    if parameters == False:
        print("the same parameters are not available in all files")


    results = []
    for ff in self.current:
        cdo_result = os.popen( "cdo griddes " + ff).read()
        results.append(cdo_result)
        

    if len(list(set(results))) == 1:
        grid = True
    else:
        grid = False 

    if grid == False:
        print("the same grid is not available in all files")



    return grid or parameters
