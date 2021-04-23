
from nctoolkit.runthis import run_this


def fill_na(self, n = 1):
    """
    Fill missing values with distance-weighted average.
    Parameters
    -------------
    n: int
        Number of nearest neighbours to use. Defaults to 1.
    """

    cdo_command = f"cdo -setmisstodis,{n}"

    run_this(cdo_command, self, output="ensemble")
