from nctoolkit.runthis import run_this


def fill_na(self, n=1):
    """
    Fill missing values with a distance-weighted average. This carries out infilling for each time step and vertical level.

    Parameters
    -------------
    n: int
        Number of nearest neighbours to use. Defaults to 1. To
    """

    cdo_command = f"cdo -setmisstodis,{n}"

    run_this(cdo_command, self, output="ensemble")
