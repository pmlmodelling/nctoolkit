
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from .flatten import str_flatten
from ._depths import nc_depths 
from ._variables import variables
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._cleanup import cleanup
from ._runcommand import run_command

def clip(self, vars = None, lon_range = [-180, 180], lat_range = [-90, 90], vert_range = None, months = None, years = None,  cdo_output = False):
    """ Function to clip netcdf files, spatially and temporally"""
    ff = self.current
    if type(ff) is not str:
        raise ValueError("The current state of the tracker is not a string")
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    ff_orig = os.path.abspath(ff)
    os.chdir("/tmp")
    
    global nc_created

    nc_created.append(self.target)
# check the validity of the ranges supplied
    
    if (type(lon_range) is not list) or (type(lat_range) is not list):
        raise ValueError("Check that lon/lat ranges are tuples")
    
    if( type(lon_range[0]) is float ) or ( type(lon_range[0]) is int) == False:
        raise ValueError("Check lon_range")
    
    if( type(lon_range[1]) is float ) or ( type(lon_range[1]) is int) == False:
        raise ValueError("Check lon_range")

    if( type(lat_range[0]) is float ) or ( type(lat_range[0]) is int) == False:
        raise ValueError("Check lat_range")
    
    if( type(lat_range[1]) is float ) or ( type(lat_range[1]) is int) == False:
        raise ValueError("Check lat_range")

# check the vert_range, if supplied, is a typle

    if vert_range is not None:
        if type(vert_range) is not list:
            raise ValueError("vert_range supplied is not a tuple")

        if ((type(vert_range[0]) is float ) or ( type(vert_range[0]) is int)) == False:
            print(type(vert_range[0]) is float)
            raise ValueError("Check vert_range 1")

        if ((type(vert_range[1]) is float ) or ( type(vert_range[1]) is int)) == False:
            raise ValueError("Check vert_range 2")

        if vert_range[1] < vert_range[0]:
            raise ValueError("vert_depths are invalid")

        if vert_range is not None:
            if type(vert_range) is not list:
                raise ValueError("vert_range supplied is not a tuple")

# check the months are valid

    if type(months) is int:
        months = [months]

    if type(months) is not list and months is not None:
        raise ValueError("months is not a valid format")

# now, we need to iterate through the months supplied
    
    valid_months = list(range(1, 13))

    if months is not None:
        for mm in months:
            if mm not in valid_months:
                raise ValueError("Check that months supplied are months")
 
# check the months are valid

    if type(years) is int:
        years = [years]

    if type(years) is not list and years is not None:
        raise ValueError("years is not a valid format")

# now, we need to iterate through the months supplied
    
    if years is not None:
        for yy in years:
            if type(yy) is not int:
                raise ValueError("Check that years supplied are integers")
        
    # a check needs to be added here for the number of grids in the netcdf file

    try:
    #    if out_file is not None:
    #        out_file  = os.path.abspath(out_file)
    # need a check at this point for file validity     
        holding_nc = ff_orig
        temp_nc = tempfile.NamedTemporaryFile().name + ".nc"
        dummy_nc = tempfile.NamedTemporaryFile().name + ".nc"
        nc_created.append(temp_nc)
        nc_created.append(dummy_nc)
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
         
         # Now, we need to select the variables we are interested in....
        if vars != None:
            cdo_call = ("cdo selname," + str_flatten(vars) + " " + holding_nc + " " + dummy_nc)
            self.history.append(cdo_call)
            run_command(cdo_call)
            if holding_nc == ff_orig:
               holding_nc = temp_nc

         # throw error if selecting vars fails
            if os.path.isfile(dummy_nc) == False:
                raise ValueError("variable selection did not work. Check output")
             
            os.rename(dummy_nc, holding_nc)

        # now, clip to the lonlat box we need

        if lon_range[0] > -180 or lon_range[1] > 180 or lat_range[0] > -90 or lat_range[1] < 90:

            lat_box = str_flatten(lon_range + lat_range)
            cdo_call = ("cdo sellonlatbox," + lat_box + " " + holding_nc + " " + dummy_nc)
            self.history.append(cdo_call)
            run_command(cdo_call)

            if os.path.isfile(dummy_nc) == False:
                raise ValueError("horizontal remapping did not work. Check output")
           
            if holding_nc == ff_orig:
                holding_nc = temp_nc

            os.rename(dummy_nc, holding_nc)

        # now we need to clip to the vertical levels desired

        if vert_range is not None:
            depths = nc_depths(holding_nc)
            depths = depths[depths <= vert_range[1]]
            depths = depths[depths >= vert_range[0]]
            if(len(depths) == 0):
                raise ValueError("There are no depths in the range chosen")

            levels_selected = str_flatten(depths)

            cdo_call = ("cdo sellevel," + levels_selected + " " + holding_nc + " " + dummy_nc)
            self.history.append(cdo_call)
            run_command(cdo_call)

            if os.path.isfile(dummy_nc) == False:
                raise ValueError("horizontal remapping did not work. Check output")
          
            if holding_nc == ff_orig:
                holding_nc = temp_nc

            os.rename(dummy_nc, holding_nc)

        if months is not None:
            cdo_output = os.popen("cdo showmon " + holding_nc).read()
            cdo_output= cdo_output.split()

            cdo_output = [int(mm) for mm in cdo_output]
            cdo_output = list(set(cdo_output))

            month_clip = True
            if any(elem in cdo_output for elem in months) == False:
                print("warning: none of the months are in the netcdf file. Skipping monthly clipping!")
                month_clip = False

            if all(elem in cdo_output for elem in months) == False and month_clip == True:
                print("warning: not all months are available in the netcdf file")
            
            if month_clip:
                month_choice = str_flatten(months)
                cdo_call = ("cdo selmonth," + month_choice + " " + holding_nc + " " + dummy_nc)
                self.history.append(cdo_call)
                run_command(cdo_call)

                if os.path.isfile(dummy_nc) == False:
                    raise ValueError("monthly clipping did not work. Check output")
          
                if holding_nc == ff_orig:
                    holding_nc = temp_nc

                os.rename(dummy_nc, holding_nc)

        # now clip to the years required


        if years is not None:
            cdo_output = os.popen("cdo showyear " + holding_nc).read()
            cdo_output= cdo_output.split()

            cdo_output = [int(mm) for mm in cdo_output]
            cdo_output = list(set(cdo_output))

            year_clip = True
            if any(elem in cdo_output for elem in years) == False:
                print("warning: none of the years are in the netcdf file. Skipping yearly clipping!")
                year_clip = False

            if all(elem in cdo_output for elem in years) == False and year_clip == True:
                print("warning: not all years are available in the netcdf file")
            
            if year_clip:
                year_choice = str_flatten(years)
                cdo_call = ("cdo selyear," + year_choice + " " + holding_nc + " " + dummy_nc)
                self.history.append(cdo_call)
                run_command(cdo_call)

                if os.path.isfile(dummy_nc) == False:
                    raise ValueError("yearly clipping did not work. Check output")
          
                if holding_nc == ff_orig:
                    holding_nc = temp_nc

                os.rename(dummy_nc, holding_nc)

        os.rename(holding_nc, self.target)

        self.current = self.target 

        # clean up the directory
        cleanup(keep = self.current)

        return(self)
    

    finally:
         os.chdir(owd)
    
