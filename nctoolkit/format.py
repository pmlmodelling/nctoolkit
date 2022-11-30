from nctoolkit.session import session_info


def format(self, ext=None):
    """
    Zip the dataset
    This will compress the files within the dataset. This works lazily.

    Parameters
    -------------
    ext: str
        New format. Must be one of "nc", "nc1", "nc2",  "nc4" and "nc5" .
        netCDF = nc1
        netCDF version 2 (64-bit offset) = nc2/nc
        netCDF4 (HDF5) = nc4
        netCDF4-classi = nc4c
        netCDF version 5 (64-bit data) = nc5
    """

    if ext is None:
        raise ValueError("Please supply a format type")

    if not isinstance(ext, str):
        raise TypeError("Please supply a valid format type")

    if ext not in ["nc", "nc1", "nc2", "nc4", "nc4c", "nc5"]:
        raise ValueError(f"{ext} is not a valid format!")

    self._format = ext

    if session_info["lazy"] is False:
        self._execute = False
        self.run()
