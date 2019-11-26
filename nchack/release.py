
import os
import copy

from .runthis import run_this
from .session import session_info

def release(self,  run_merge = True):
    """
    Run all stored commands in a dataset

    Parameters
    -------------
    run_merge: boolean
        Ignore this for now. This needs to be replaced by the keywords arg method

    """

    # the first step is to set the run status to true

    if self.run == False and (len(self.history) > len(self._hold_history)):
        self.run = True
        self.released = True

        if (len(self.history) > len(self._hold_history)) and session_info["thread_safe"] == False:
            cdo_command = "cdo -L"
        else:
            cdo_command = "cdo "

        output_method = "ensemble"

        if self.merged:
            output_method = "one"

        run_this(cdo_command, self,  output = output_method)
        self.released = False

        self.run = False



