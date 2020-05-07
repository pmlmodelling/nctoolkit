
import os
from .cleanup import cleanup
from .runthis import run_this
from .api import open_data

def reduce_grid(self, mask):
    """
    Reduce to non-zero locations in mask
    Parameters
    -------------
    mask: str or dataset
        single variable dataset or path to .nc file

    """

    target = None

    if type(mask) is str:
        if os.path.exists(mask) == False:
            raise ValueError(f"{mask} does not exist")

        target = mask

    if "api.DataSet" in str(type(mask)):
        target = mask.current
        self._safe.append(mask)

    if target is None:
        raise ValueError("No mask supplied")


    targeted_mask = open_data(target)
    targeted_mask.cdo_command("-setmisstoc,0")
    targeted_mask.run()

    cdo_command = f"cdo -reducegrid,{targeted_mask.current}"

    run_this(cdo_command, self, output = "ensemble")

