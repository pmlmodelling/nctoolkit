
from ._cleanup import cleanup
from ._runthis import run_this

def merge(self, silent = True):
    """Function to merge a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

   # log the full path of the file

    cdo_command = ("cdo merge")

    run_this(cdo_command, self, silent, output = "one") 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
