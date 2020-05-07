from .runthis import run_this
from .session import session_info
from .session import nc_safe
from .cleanup import cleanup

def release(self,  run_merge = True):
    """
    Run all stored commands in a dataset

    Parameters
    -------------
    run_merge: boolean
        Ignore this for now. This needs to be replaced by the keywords arg method

    """

    # the first step is to set the run status to true

    if (self._execute == False) and (len(self.history) > len(self._hold_history)):
        self._execute = True

        cdo_command = "cdo "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self,  output = output_method)

        self._merged = False

        self._execute = False
        self._zip = False

        if len(self._safe) > 0:
            for ff in self._safe:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        self._safe = []

        cleanup()





