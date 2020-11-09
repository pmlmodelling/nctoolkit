from nctoolkit.runthis import run_this


def format(self, ext = None):
    """
    Zip the dataset
    This will compress the files within the dataset. This works lazily.
    Parameters
    -------------
    ext: str
        New format. Must be one of "nc", "nc1", "nc2",  "nc4" and "nc5" .
        NetCDF = nc1
        NetCDF version 2 (64-bit offset) = nc2/nc
        NetCDF4 (HDF5) = nc4
        NetCDF4-classi = nc4c
        NetCDF version 5 (64-bit data) = nc5
    """

    if ext is None:
        raise ValueError("Please supply a format type")

    if type(ext) is not str:
        raise ValueError("Please supply a valid format type")

    if ext not in ["nc", "nc1", "nc2", "nc4", "nc4c", "nc5"]:
        raise ValueError(f"{ext} is not a valid format!")


    self._format = ext

