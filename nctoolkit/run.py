from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this
from nctoolkit.session import remove_safe


def run(self):
    """
    Run all stored commands in a dataset

    Examples
    ------------
    If evaluation is lazy and you need to evaluate commands on a dataset, do the following:

    >>> ds.run()

    """

    # the first step is to set the run status to true

    if (self._execute is False) and (
        len(self.history) > len(self._hold_history)
        or self._zip
        or self._format is not None 
        or self._precision != "default"
    ):
        self._execute = True

        cdo_command = "cdo "
        if self._precision != "default":
            if len(self.history) == len(self._hold_history):
                cdo_command = "cdo copy "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self, output=output_method)

        self._merged = False

        self._execute = False
        self._zip = False

        if len(self._safe) > 0:
            for ff in self._safe:
                remove_safe(ff)

        self._safe = []

        cleanup()

        self._ncommands = 0
        self._align= ""
        self.disk_clean()

        self._precision = "default"
