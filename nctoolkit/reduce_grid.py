import os

from nctoolkit.api import open_data
from nctoolkit.runthis import run_this
import nctoolkit.api as api


def reduce_grid(self, mask=None):
    """
    Reduce the dataset to non-zero locations in a mask

    Parameters
    -------------
    mask: str or dataset
        single variable dataset or path to .nc file.
        The mask must have an identical grid to the dataset.
    """

    target = None

    # pull out the mask file
    if isinstance(mask, str):
        if os.path.exists(mask) is False:
            raise ValueError(f"{mask} does not exist")
        target = mask

    if isinstance(mask, api.DataSet):
        target = mask.current[0]

    if target is None:
        raise ValueError("No mask supplied")

    # Set missing values to zero in the mask, just in case
    targeted_mask = open_data(target)
    targeted_mask.cdo_command("-setmisstoc,0")
    targeted_mask.run()

    cdo_command = f"cdo -reducegrid,{targeted_mask.current[0]}"

    run_this(cdo_command, self, output="ensemble")
    self.run()
