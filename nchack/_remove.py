
import os

def nc_remove(ff):
    """ Function for removing netcdf files. This is ultra-safe and makes sure the file is in the tmp directory before deleting""" 
    if ff.startswith("/tmp") == False:
        raise ValueError("The file " + ff + " is not in the tmp folder")
    os.remove(ff)
        
