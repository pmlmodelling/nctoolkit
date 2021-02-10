from nctoolkit.runthis import run_this
from nctoolkit.temp_file import temp_file
from nctoolkit.runthis import run_cdo
from nctoolkit.session import remove_safe, get_safe
from nctoolkit.cleanup import cleanup
import warnings
import os



def gt(self, ff):
    """
    Method to calculate if variable in dataset is greater than that in another file

    Parameters
    -------------
    ff: str
        File path

    """

    if os.path.exists(ff) == False:
        raise ValueError(f"{ff} does not exist!")

    self.run()

    if len(self) > 1:
        raise ValueError("This only works on single file datasets currently!")

    temp = temp_file(".nc")

    cdo_command = f"cdo -gt {self[0]} {ff} {temp}"

    target = run_cdo(cdo_command, temp)

    self.current = target

    if len([x for x in get_safe() if x == target]) > 1:
        remove_safe(target)

    cleanup()



