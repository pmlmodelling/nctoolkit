
# to do
# think about adding ability to call nco

from ._cleanup import cleanup
from ._runthis import run_this

def ensemble_percentile(self, p = 50, silent = True):
    """Function to calculate an ensemble percentile from a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo enspctl," + str(p)

    run_this(cdo_command, self, silent, output = "one")

    # clean up the directory
    cleanup(keep = self.current)

    return self
