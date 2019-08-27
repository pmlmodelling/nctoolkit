
import os
import tempfile
# function to get the depths available in a netcdf file

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


