from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this
from nctoolkit.session import nc_safe
import warnings


def run(self):
    """
    Run all stored commands in a dataset
    """

    # the first step is to set the run status to true

    if (self._execute is False) and (
        len(self.history) > len(self._hold_history) or self._zip
    ):
        self._execute = True

        cdo_command = "cdo "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self, output=output_method)

        self._merged = False

        self._execute = False
        self._zip = False

        if len(self._safe) > 0:
            for ff in self._safe:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        self._safe = []

        cleanup()

        self._ncommands = 0
