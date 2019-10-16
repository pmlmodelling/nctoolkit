import os
import copy
import multiprocessing

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
from ._cleanup import cleanup
from ._setters import set_longname
from ._runthis import run_cdo
import copy


def phenology(self, var = None, silent = False, cores = 1):
    """
    Method to calculate the phenology of a variable.
    At present this only works for one variable, which should be enough.
    """

    if var is None:
        raise ValueError("No var was supplied")
    if type(var) is not str:
        raise ValueError("var is not a str")

    # First step is to check if the current file exists
    if type(self.current) is str:
        if os.path.exists(self.current) == False:
            raise ValueError("The file " + self.current + " does not exist!")
    else:
        raise ValueError("This method only works on single files")

    #  create a new tracker for the phenologies
    # Then restrict the file to the var selected
    
    new_self = copy.deepcopy(self)
    
    new_self.select_variables(var)

    # Create the day of year

    doy_nc = temp_file("nc")
    nc_created.append(doy_nc)
    
    cdo_command = "cdo -L -timcumsum -chname," + var +   ",peak -setclonlatbox,1,-180,180,-90,90 " + new_self.current + " " + doy_nc

    new_self.history.append(cdo_command)

    doy_nc = run_cdo(cdo_command, doy_nc)

    if os.path.exists(doy_nc) == False:
        raise ValueError("Creating day of year failed")

    # Find the max value of the var

    max_nc = temp_file("nc") 
    nc_created.append(max_nc)

    cdo_command = "cdo -L -timmax -chname," + var + "," + var + "_max " + new_self.current + " " + max_nc

    new_self.history.append(cdo_command)
    max_nc = run_cdo(cdo_command, max_nc)

    if os.path.exists(max_nc) == False:
        raise ValueError("Calculating the max of " + var + " failed!")

    # We now need to merge the three  netcdf files

    out_nc = temp_file("nc")
    nc_created.append(out_nc)

    
    cdo_command = "cdo merge " + new_self.current + " " + max_nc + " " + doy_nc + " " + out_nc

    new_self.history.append(cdo_command)
    out_nc = run_cdo(cdo_command, out_nc)

    if os.path.exists(out_nc) == False:
        raise ValueError("Merging netcdf files failed!")

    # Now, calculate the timing of the annual maximum

    phen_nc = temp_file("nc") 
    nc_created.append(phen_nc)

    cdo_command = "cdo -L -timmin -selname,peak -expr,'peak=peak + 365*(" + var + "<" + var + "_max)' " + out_nc + " " + phen_nc

    new_self.history.append(cdo_command)
    phen_nc = run_cdo(cdo_command, phen_nc)

    if os.path.exists(phen_nc) == False:
        raise ValueError("Failed to merge files")

    new_self.current = phen_nc

    # set the long name and unit

    new_self.set_longname({"peak": "Timing of annual maximum"})

    new_self.set_unit({"peak": "Day of year"})

    cleanup(new_self.current)

    return new_self



