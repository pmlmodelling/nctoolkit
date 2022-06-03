import os
import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.session import remove_safe


def to_nc(self, out, zip=True, overwrite=False, **kwargs):
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
    **kwargs : kwargs
        Optional arguments to be sent to subset.

    Examples
    ------------
    If you want to export a dataset to a netCDF file, do the following:

        >>> ds.to_nc("out.nc")

    By default this file will be zipped. If you do not want it zipped, do this:

        >>> ds.to_nc("out.nc", zip = False)

    By default this cannot overwrite files. If the output file exists, do the following:

        >>> ds.to_nc("out.nc", overwrite = True)

    If you only want to export a subset of the data, you can use optional arguments that will be sent to subset.
    For example, if you only wanted the year 2000, you would do this:

        >>> ds.to_nc("out.nc", year = 2000)


    """

    if len(self) == 0:
        raise ValueError("You cannot save an empty dataset!")

    if os.path.basename(out) != out:
        out_dir = os.path.dirname(out)
        if os.path.exists(out_dir) is False:
            raise ValueError(f"{out_dir} does not exist!")


    # Figure out if it is possible to write the file, i.e. if a dataset is still an
    # ensemble, you cannot write.
    ff = copy.deepcopy(self.current)
    write = False

    if len(self) == 1:
        write = True

    if self._merged:
        write = True

    if write is False:
        raise ValueError("You cannot save multiple files!")

    if (os.path.exists(out)) and (overwrite is True):
        if len(self) > 1:
            self.run()


    # Check if outfile exists and overwrite is set to False
    # This should maybe be a warning, not an error
    if (os.path.exists(out)) and (overwrite is False):
        raise ValueError("The out file exists and overwrite is set to false")


    if len(kwargs) > 0:

        self1 = self.copy()

        self1.subset(**kwargs)

        self1.run()
        ff = copy.deepcopy(self1.current)


        if len(self1.history) == len(self1._hold_history):
            if zip:
                cdo_command = f"cdo -z zip_9 copy {ff[0]} {out}"
                run_cdo(
                    cdo_command, target=out, overwrite=overwrite, precision=self._precision
                )

                self1.history.append(cdo_command)
                self1._hold_history = copy.deepcopy(self1.history)
                self1.current = out
                remove_safe(out)

            else:
                cdo_command = f"cdo copy {ff[0]} {out}"
                run_cdo(
                    cdo_command, target=out, overwrite=overwrite, precision=self1._precision
                )
                self1.history.append(cdo_command)
                self1._hold_history = copy.deepcopy(self1.history)

                self1.current = out
                remove_safe(out)

        else:
            if zip:
                cdo_command = "cdo -z zip_9 "
            else:
                cdo_command = "cdo "

            self1._execute = True

            run_this(cdo_command, self1, out_file=out)
            self1._execute = False

        if os.path.exists(out) is False:
            raise ValueError("File zipping was not successful")
    else:

        ff = copy.deepcopy(self.current)

        if len(self.history) == len(self._hold_history):
            if zip:
                cdo_command = f"cdo -z zip_9 copy {ff[0]} {out}"
                run_cdo(
                    cdo_command, target=out, overwrite=overwrite, precision=self._precision
                )
                self.history.append(cdo_command)
                self._hold_history = copy.deepcopy(self.history)
                self.current = out
                remove_safe(out)


            else:
                cdo_command = f"cdo copy {ff[0]} {out}"
                run_cdo(
                    cdo_command, target=out, overwrite=overwrite, precision=self._precision
                )
                self.history.append(cdo_command)
                self._hold_history = copy.deepcopy(self.history)

                self.current = out
                remove_safe(out)

        else:
            if zip:
                cdo_command = "cdo -z zip_9 "
            else:
                cdo_command = "cdo "

            self._execute = True
            run_this(cdo_command, self, out_file=out)
            self._execute = False
            self.current = out

        if os.path.exists(out) is False:
            raise ValueError("File zipping was not successful")


    cleanup()
