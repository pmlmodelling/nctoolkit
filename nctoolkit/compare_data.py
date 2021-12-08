from nctoolkit.runthis import run_this
from nctoolkit.temp_file import temp_file
from nctoolkit.runthis import run_cdo
from nctoolkit.session import remove_safe, get_safe
from nctoolkit.cleanup import cleanup
import warnings
import os


def lt(self, x):
    """
    Method to calculate if variable in dataset is less than that in another file or dataset
    This currently only works with single file datasets

    Parameters
    -------------
    x: str or single file dataset
        File path or nctoolkit dataset

    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    self.run()

    x_ff = None

    new_files = []

    for ff in self:

        if "api.DataSet" in str(type(x)):
            x.run()
            if len(x) != 1:
                raise ValueError("This only works on single file datasets")
            x_ff = x[0]

        if type(x) is str:
            x_ff = x

        if x_ff is None:
            raise ValueError("ff needs to be a file path or nctoolkit dataset")

        if os.path.exists(x_ff) == False:
            raise ValueError(f"{x_ff} does not exist!")

        temp = temp_file(".nc")

        cdo_command = f"cdo -lt {ff} {x_ff} {temp}"

        target = run_cdo(cdo_command, temp, precision=self._precision)
        new_files.append(target)

    self.history.append(cdo_command)
    self._hold_history.append(cdo_command)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()


def gt(self, x):
    """
    Method to calculate if variable in dataset is greater than that in another file or dataset
    This currently only works with single file datasets

    Parameters
    -------------
    x: str or single file dataset
        File path or nctoolkit dataset

    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    self.run()

    x_ff = None

    new_files = []

    for ff in self:

        if "api.DataSet" in str(type(x)):
            x.run()
            if len(x) != 1:
                raise ValueError("This only works on single file datasets")
            x_ff = x[0]

        if type(x) is str:
            x_ff = x

        if os.path.exists(x_ff) == False:
            raise ValueError(f"{x_ff} does not exist!")

        if x_ff is None:
            raise ValueError("ff needs to be a file path or nctoolkit dataset")

        temp = temp_file(".nc")

        cdo_command = f"cdo -gt {ff} {x_ff} {temp}"

        target = run_cdo(cdo_command, temp, precision=self._precision)
        new_files.append(target)

    self.history.append(cdo_command)
    self._hold_history.append(cdo_command)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()
