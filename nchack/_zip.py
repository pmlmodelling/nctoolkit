
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def zip(self):
    """
    Zip the dataset

    """

    if self.run == True:
        cdo_command = "cdo -z zip copy "
    else:
        cdo_command = "cdo -z zip "
    run_this(cdo_command, self, output = "ensemble")

