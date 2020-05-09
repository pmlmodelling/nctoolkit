import os
import copy

from .cleanup import cleanup
from .runthis import run_this
from .runthis import run_cdo
from .session import nc_safe
from .session import session_info


def write_nc(self, out, zip=True, overwrite=False):
    """
    Save a dataset to a named file

    Parameters
    -------------
    out : str
        output file name
    zip : boolean
        True/False depending on whether you want to zip the file. Defaults to True.

    """

    # If the output file exists, cdo cannot simultaneously have it opened and written to
    if (os.path.exists(out)) and (overwrite == True):
        self.run()

    if type(self.current) is list:
        ff = copy.deepcopy(self.current)
    else:
        ff = [copy.deepcopy(self.current)]

    write = False

    if type(self.current) is str:
        write = True

    if self._merged:
        write = True

    if write == False:
        raise ValueError("You cannot save multiple files!")

    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error
    if (os.path.exists(out)) and (overwrite == False):
        raise ValueError("The out file exists and overwrite is set to false")

    if len(self.history) == len(self._hold_history):
        if zip:
            cdo_command = f"cdo -z zip_9 copy {ff[0]} {out}"
            os.system(cdo_command)
            self.history.append(cdo_command)
            self._hold_history = copy.deepcopy(self.history)
            self.current = out

        else:
            cdo_command = f"cdo copy {ff[0]} {out}"
            os.system(cdo_command)
            self.history.append(cdo_command)
            self._hold_history = copy.deepcopy(self.history)

            self.current = out

    else:
        if zip:
            cdo_command = "cdo -z zip_9 "
        else:
            cdo_command = "cdo "

        self._execute = True

        run_this(cdo_command, self, out_file=out)
        self._execute = False

    if os.path.exists(out) == False:
        raise ValueError("File zipping was not successful")

    self.current = out

    cleanup()
