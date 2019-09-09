import os

# function to get list of variables

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

