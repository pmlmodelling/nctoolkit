
import os

def nc_remove(ff):
    """Method for removing netcdf files. This is ultra-safe and makes sure the file is in the tmp directory before deleting""" 
    if (ff.startswith("/tmp") or ff.startswith("/var/tmp/") or ff.startswith("/usr/tmp/")) == False:
        raise ValueError("The file " + ff + " is not in a tmp folder")
    os.remove(ff)
        
