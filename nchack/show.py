
import subprocess
import pandas as pd
import numpy as np


def times(self):

    if type(self.current) is str:
        file_list = [self.current]
    else:
        file_list = self.current
    all_times = []
    for ff in file_list:
        cdo_result = subprocess.run("cdo showtimestamp " + ff, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_times+=cdo_result
    all_times = list(set(all_times))
    all_times.sort()
    return all_times
#
#def times(self):
#    if type(self.current) is list:
#        raise TypeError("This presently only works for single file datasets")
#
#    cdo_result = subprocess.run("cdo showtimestamp " + self.current, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    cdo_result = str(cdo_result.stdout).replace("\\n", "")
#    cdo_result = cdo_result.replace("b'", "").strip()
#    cdo_result = cdo_result.replace("'", "").strip()
#    cdo_result = cdo_result.split()
#    cdo_result = pd.Series( (v for v in cdo_result) )
#
#    return cdo_result

def levels(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")
    """
    Method to get the depths available in a netcdf file
    """
    cdo_result = subprocess.run("cdo showlevel " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [float(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result


def nc_variables(ff):
    cdo_result = subprocess.run("cdo showname " + ff, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    return cdo_result

def years(self):

    if type(self.current) is str:
        file_list = [self.current]
    else:
        file_list = self.current
    all_years = []
    for ff in file_list:
        cdo_result = subprocess.run("cdo showyear " + ff, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_years+=cdo_result
    all_years = list(set(all_years))
    all_years =  [int(v) for v in all_years]
    all_years.sort()
    return all_years


def months(self):

    if type(self.current) is str:
        file_list = [self.current]
    else:
        file_list = self.current
    all_months = []
    for ff in file_list:
        cdo_result = subprocess.run("cdo showmon " + ff, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_months+=cdo_result
    all_months = list(set(all_months))
    all_months =  [int(v) for v in all_months]
    all_months.sort()
    return all_months


def attributes(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    out = subprocess.run("cdo showatts " + self.current, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = out.stdout.decode('utf-8')
    return out

def global_attributes(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    out = subprocess.run("cdo showattsglob " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    out = out.stdout.decode('utf-8')
    return out

