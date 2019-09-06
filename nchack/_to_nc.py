import os
import shutil

from ._cleanup import cleanup
from ._runcommand import run_command

def to_netcdf(self, out, zip = True, overwrite = False):
    """ Function to save the current file to netcdf"""
    ff = self.current
    if type(ff) is not str:
        raise ValueError("The current state of the tracker is not a string")

    if os.path.exists(ff) == False: 
        raise ValueError("The current state of the tracker does not exist")

    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error 
    if os.path.exists(out) and overwrite == False: 
        raise ValueError("The out file exists and overwrite is set to false")
    if zip:
        os.system("cdo -f nc4 -z zip_9 copy " + ff + " " + out)
        if os.path.exists(out) == False: 
            raise ValueError("File zipping was not successful")
    else:
        shutil.copy(ff, out)

    # run the cleanup
    cleanup()

   
