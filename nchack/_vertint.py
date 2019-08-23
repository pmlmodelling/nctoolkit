
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


def vertical_interp(self, vert_depths = None, silent = True):
    owd = os.getcwd()
   # log the full path of the file
    ff_orig = os.path.abspath(self.current)
    os.chdir("/tmp")
    try:
    # need a check at this point for file validity     
        target = tempfile.NamedTemporaryFile().name + ".nc"
        holding_nc = ff_orig 
        temp_nc = target 
        dummy_nc = tempfile.NamedTemporaryFile().name + ".nc"
        nc_created.append(target)
        nc_created.append(dummy_nc)
        nc_created.append(target)
         
        vertical_remap = False


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
            cdo_command = ("cdo intlevel," + vert_depths + " " + holding_nc + " " + dummy_nc)
            self.history(cdo_command)
            run_command(cdo_command, self, silent)

            if holding_nc == ff_orig:
                holding_nc = temp_nc

         # throw error if cdo fails at this point
        
            os.rename(dummy_nc, holding_nc)
        if vertical_remap:
            
            if self.run: self.current = target 
        
        cleanup(keep = self.current)
        


        return(self)


    finally:
         os.chdir(owd)
