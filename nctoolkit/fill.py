def fill_na(self, n=1):
    """
    fill_na: Fill missing values with a distance-weighted average. This carries out infilling for each time step and vertical level.

    Filling only uses horizontal neighbours, not vertical.

    Parameters
    -------------
    n: int
        Number of nearest neighbours to use. Defaults to 1. To

    Examples
    -------------
    Fill missing values with a distance-weighted average using 5 nearest neighbours:
        >>> ds.fill_na(n=5)




    """

    cdo_command = f"-setmisstodis,{n}"

    self.cdo_command(command=cdo_command, ensemble=False)
