import os
import tempfile
from ._cleanup import cleanup
from ._runthis import run_this
from .flatten import str_flatten
from ._filetracker import nc_created
from ._runcommand import run_command
import pandas as pd
import calendar
from datetime import datetime
import time

def year_days(x):
    if calendar.isleap(x):
        return 366
    else:
        return 365

# Ensemble methods all assume the structure of the input files are idential
# So the time steps should be the same
# e.g. it could be an ensemble of climate models with the same variables and same times
# or it could be daily files for an entire year and you want the annual mean etc.
# Is there a way to check the ensemble without it being slow?


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

def check_dates(self):
    "A function to check if sufficient dates are available in a file or ensemble"
    if type(self.current) is str:
        ensemble = [self.current]
    else:
        ensemble = self.current

    all_times = []
    for ff in ensemble:
        cdo_result = os.popen( "cdo showdate " + ff).read()
        cdo_result = cdo_result.replace("\n", "")
        cdo_result = cdo_result.split()
        cdo_result = pd.Series( (datetime.strptime(v, "%Y-%m-%d") for v in cdo_result) )
        all_times.append(cdo_result)
    
    all_times = pd.concat(all_times)
    
    if len(all_times)/len(all_times.drop_duplicates()) > 1:
        print("There are duplicate times")
    df = pd.DataFrame({"date":all_times})
    df["year"] = [x.year for x in all_times]
    df = df.groupby("year").size().reset_index()
    df.columns = ["year", "dates_available"]
    df["days_in_year"] = [year_days(x) for x in df.year]
    df = df.filter(["year", "days_in_year", "dates_available"])

    return(df)






