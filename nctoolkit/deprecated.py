
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

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only file in the dataset. No need to merge!")
        return None

    cdo_command = "cdo --sortname -mergetime"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True
