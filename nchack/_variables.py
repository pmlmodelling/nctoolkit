import os

# function to get list of variables

def variables(self, detailed = False):
    cdo_result = os.popen( "cdo showname " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
  #  if detailed == False:
    return(cdo_result)
