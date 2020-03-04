
from .cleanup import cleanup
from .runthis import run_this

def zip(self):
    """
    Zip the dataset

    """
    self._zip = True

    if len(self.history) == len(self._hold_history):
        cdo_command = "copy "
        run_this(cdo_command, self, output = "ensemble")

