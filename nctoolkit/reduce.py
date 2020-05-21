
from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this


def reduce_dims(self):
    """
    Reduce dimensions of data
    This will remove any dimensions with only one value. For example, if only selecting one vertical level, the vertical dimension will be removed.
    """

    if len(self.history) == len(self._hold_history):
        cdo_command = "cdo --reduce_dim copy"
    else:
        cdo_command = "cdo --reduce_dim"

    run_this(cdo_command, self, output="ensemble")
