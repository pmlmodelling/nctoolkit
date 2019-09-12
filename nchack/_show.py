
import os
import pandas as pd

def times(self):
    ff = self.current
    cdo_result = os.popen( "cdo showtimestamp " + ff).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = pd.Series( (v for v in cdo_result) )
    return cdo_result

def depths(self):
    """function to get the depths available in a netcdf file"""
    cdo_result = os.popen( "cdo showlevel " + self.current).read()
    cdo_result = cdo_result.replace("\n", "").split()
    cdo_result = pd.Series( (float(v) for v in cdo_result) )
    cdo_result = pd.Series.unique(cdo_result)
    return cdo_result

def numbers(self):
    ff = self.current
    npar = int(os.popen( "cdo npar " + ff).read().split("\n")[0])
    nlevel = int(os.popen( "cdo nlevel " + ff).read().split("\n")[0])
    nyear = int(os.popen( "cdo nyear " + ff).read().split("\n")[0])
    nmon = int(os.popen( "cdo nmon " + ff).read().split("\n")[0])
    ndate = int(os.popen( "cdo ndate " + ff).read().split("\n")[0])
    ntime = int(os.popen( "cdo ntime " + ff).read().split("\n")[0])
    ngridpoints = int(os.popen( "cdo ngridpoints " + ff).read().split("\n")[0])
    ngrids = int(os.popen( "cdo ngrids " + ff).read().split("\n")[0])
    output = "Number of variables: " + str(npar) + "\n"
    output += "Number of levels: " + str(nlevel) + "\n"
    output += "Number of years: " + str(nyear) + "\n"
    output += "Number of months: " + str(nmon) + "\n"
    output += "Number of dates: " + str(ndate) + "\n"
    output += "Number of times: " + str(ntime) + "\n"
    output += "Number of grid points: " + str(ngridpoints) + "\n"
    output += "Number of horizontal grids: " + str(ngrids)
    
    print(output)

def variables(self, detailed = False):
    cdo_result = os.popen( "cdo showname " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()

    return cdo_result

def nc_variables(ff):
    cdo_result = os.popen( "cdo showname " + ff).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()

    return cdo_result


def variables(self, detailed = False):
    cdo_result = os.popen( "cdo showname " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()

    return cdo_result

def nc_variables(ff):
    cdo_result = os.popen( "cdo showname " + ff).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()

    return cdo_result


def show_years(self):
    cdo_result = os.popen( "cdo showyear " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result

def show_months(self):
    cdo_result = os.popen( "cdo showmon " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    cdo_result = [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result

def show_levels(self):
    cdo_result = os.popen( "cdo showlevel " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    cdo_result = [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result


