def invert(self, x=None):
    """
    invert: Invert levels or latitudes

    Parameters
    -------------
    x: str
        What you want to invert. Either "levels" or "latitudes"
        Note: this is reasonably fuzzy so anything with "lev" or "lat" will work

    Examples
    -------------
    If you want to invert the vertical levels of a file, you can do the following:
    >>> cdo.invert("levels")
    If you want to invert the latitudes of a file, you can do the following:
    >>> cdo.invert("latitudes")

    """

    # create the cdo call and run it
    if "lev" in x.lower():
        cdo_command = "-invertlev"

    elif "lat" in x.lower():
        cdo_command = "-invertlat"

    else:
        raise ValueError("x must be either levels or latitudes")

    self.cdo_command(cdo_command, ensemble=False)
