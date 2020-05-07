
from .cleanup import cleanup
from .runthis import run_this

def reduce_dims(self):
    """
    Reduce dimensions of data
    Reduce dimensions of data. For example, if only selecting one vertical level, the vertical dimension will be removed.
    """

    if len(self.history) == len(self._hold_history):
        cdo_command = "cdo --reduce_dim copy"
    else:
        cdo_command = "cdo --reduce_dim"

    run_this(cdo_command, self, output = "ensemble")

