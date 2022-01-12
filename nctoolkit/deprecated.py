
import pandas as pd
import subprocess
import warnings

from datetime import datetime

from nctoolkit.runthis import run_this
from nctoolkit.session import session_info
def merge_time(self):
    """
    Time-based merging of a multi-file ensemble into a single file
    This method is ideal if you have the same data split over multiple
    files covering different data sets.
    """
    warnings.warn("merge_time is deprecated. Please use merge")

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only file in the dataset. No need to merge!")
        return None

    cdo_command = "cdo --sortname -mergetime"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True

def surface(self):
    """
    Extract the top/surface level from a dataset
    This extracts the first vertical level from each file in a dataset.

    Examples
    ------------

    If you wanted to extract the top vertical level of a dataset, do the following:

    >>> ds.surface()

    This method is most useful for things like oceanic data, where this method will extract the sea surface.
    """
    warnings.warn("surface is deprecated. Please use top")

    cdo_command = "cdo -sellevidx,1"
    run_this(cdo_command, self, output="ensemble")

