
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def set_longname(self, var, new_long, silent = True):
    """Function to set the date"""

    # Check that the unit supplied is a string
    if type(new_long) is not str:
        ValueError("new_lon supplied is not a string")

    if type(new_long) is not str:
        ValueError("Only works with single vars currently")

    if type(self.current) is not str:
        ValueError("Method does not yet work with ensembles")

    if self.run == False:
        ValueError("NCO methods do not work in hold mode")

    target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)

    nco_command = "ncatted -a long_name," + var + ",o,c,'" + new_long + "' " + self.current + " " + target
    self.history.append(nco_command)

    os.system(nco_command)

    if os.path.exists(target) == False:
        raise ValueError(nco_command + " was not successful. Check output")
    self.current = target


    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
