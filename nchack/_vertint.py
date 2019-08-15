
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._depths import nc_depths
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command


def vertical_interp(self, vars = None, vert_depths = None):
    owd = os.getcwd()
   # log the full path of the file
    ff_orig = os.path.abspath(self.current)
    os.chdir("/tmp")
    try:
    # need a check at this point for file validity     
        self.target = tempfile.NamedTemporaryFile().name + ".nc"
        holding_nc = ff_orig 
        temp_nc = self.target 
        dummy_nc = tempfile.NamedTemporaryFile().name + ".nc"
        nc_created.append(self.target)
        nc_created.append(dummy_nc)
        nc_created.append(self.target)
#    # check if variables are included
         # first, a hack to make sure vars is something we can iterate over
        if vars != None:
            if type(vars) is str:
                vars = {vars}
        
        if (vars is None) == False:
            ff_variables = self.variables()
            for vv in vars:
                 if (vv in ff_variables) == False:
                     raise ValueError("variable " + vv + " is not available in the netcdf file")
         
        vertical_remap = False

        if vars != None:
            run_command("cdo selname," + str_flatten(vars) + " " + holding_nc + " " + dummy_nc)
            if holding_nc == ff_orig:
               holding_nc = temp_nc
          # throw error if selecting vars fails
            if os.path.isfile(dummy_nc) == False:
               raise ValueError("variable selection did not work. Check output")
            os.rename(dummy_nc, holding_nc)

    #  now, do the vertical remapping if necessary
    #  it is possible there are no vertical depths in the file. In this case we throw a warning message
        vertical_remap = True
           
           # first a quick fix for the case when there is only one vertical depth

        if vert_depths != None:
            if (type(vert_depths) == int) or (type(vert_depths) == float):
                vert_depths = {vert_depths}
 
        num_depths = len(nc_depths(holding_nc))
        
        if vert_depths == None:
            vertical_remap = False
        
        if vert_depths != None:
            if num_depths < 2:
                print("There are none or one vertical depths in the file. Vertical interpolation not carried out.")
                vertical_remap = False
        if ((vert_depths != None) and vertical_remap):
            available_depths = nc_depths(holding_nc)
        
        if vertical_remap:
            if (min(vert_depths) < min(available_depths)):
                 raise ValueError("error:minimum depth supplied is too low")
            if (max(vert_depths) > max(available_depths)):
                 raise ValueError("error: maximum depth supplied is too low")

            vert_depths = str_flatten(vert_depths, ",")
            run_command("cdo intlevel," + vert_depths + " " + holding_nc + " " + dummy_nc)

            if holding_nc == ff_orig:
                holding_nc = temp_nc

         # throw error if cdo fails at this point
            if os.path.isfile(dummy_nc) == False:
                raise ValueError("vertical remapping did not work. Check output")
        
            os.rename(dummy_nc, holding_nc)
        if vertical_remap:
            
            self.current = self.target 
        
        cleanup(keep = self.current)
        


        return(self)


    finally:
         os.chdir(owd)
