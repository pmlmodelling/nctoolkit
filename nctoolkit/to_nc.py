
import copy
import os

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.session import nc_safe, session_info


def write_nc(self, out, zip=True, overwrite=False):
    """
    Save a dataset to a named file
    This will only work with single file datasets.

    Parameters
    -------------
    out : str
        Output file name.
    zip : boolean
        True/False depending on whether you want to zip the file. Default is True.
    overwrite : boolean
        If out file exists, do you want to overwrite it? Default is False.
    """

    # If the output file exists, cdo cannot simultaneously have it opened and written to
    if (os.path.exists(out)) and (overwrite == True):
        self.run()

    if type(self.current) is list:
        ff = copy.deepcopy(self.current)
    else:
        ff = [copy.deepcopy(self.current)]

    # Figure out if it is possible to write the file, i.e. if a dataset is still an ensemble, you cannot write.
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
