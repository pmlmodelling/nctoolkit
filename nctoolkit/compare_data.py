from nctoolkit.runthis import run_this
from nctoolkit.temp_file import temp_file
from nctoolkit.runthis import run_cdo
from nctoolkit.session import remove_safe, get_safe
from nctoolkit.cleanup import cleanup
import warnings
import os


def gt(self, x):
    """
    Method to calculate if variable in dataset is greater than that in another file or dataset
    This currently only works with single file datasets

    Parameters
    -------------
    x: str or single file dataset
        File path or nctoolkit dataset

    """

    self.run()

    ff = None

    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) != 1:
            raise ValueError("This only works on single file datasets currently!")
        ff = x[0]

    if type(x) is str:
        ff = x

    if ff is None:
        raise ValueError("ff needs to be a file path or nctoolkit dataset")

    if os.path.exists(ff) == False:
        raise ValueError(f"{ff} does not exist!")

    if len(self) > 1:
        raise ValueError("This only works on single file datasets currently!")

    temp = temp_file(".nc")

    cdo_command = f"cdo -gt {self[0]} {ff} {temp}"

    target = run_cdo(cdo_command, temp)

    self.history.append(cdo_command)
    self._hold_history.append(cdo_command)

    self.current = target

    if len([x for x in get_safe() if x == target]) > 1:
        remove_safe(target)

    cleanup()


def lt(self, x):
    """
    Method to calculate if variable in dataset is less than that in another file or dataset
    This currently only works with single file datasets

    Parameters
    -------------
    x: str or single file dataset
        File path or nctoolkit dataset

    """

    self.run()

    ff = None

    if "api.DataSet" in str(type(x)):
        x.run()
        if len(x) != 1:
            raise ValueError("This only works on single file datasets currently!")
        ff = x[0]

    if type(x) is str:
        ff = x

    if ff is None:
        raise ValueError("ff needs to be a file path or nctoolkit dataset")

    if os.path.exists(ff) == False:
        raise ValueError(f"{ff} does not exist!")

    if len(self) > 1:
        raise ValueError("This only works on single file datasets currently!")

    temp = temp_file(".nc")

    cdo_command = f"cdo -lt {self[0]} {ff} {temp}"

    target = run_cdo(cdo_command, temp)

    self.history.append(cdo_command)
    self._hold_history.append(cdo_command)

    self.current = target

    if len([x for x in get_safe() if x == target]) > 1:
        remove_safe(target)

    cleanup()
