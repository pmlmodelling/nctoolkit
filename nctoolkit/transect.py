import numpy as np
import pandas as pd


def to_transect(self, start=None, end=None, nsteps=None, method="bil"):
    """
    to_transect: Extract a straight-line transect between two points

    Generates nsteps points along a straight line (in lon/lat space) between
    start and end, then regrids the dataset onto those points.

    Parameters
    -------------
    start: list
        [lon, lat] of the start of the transect
    end: list
        [lon, lat] of the end of the transect
    nsteps: int
        Number of points in the transect, including start and end
    method: str
        Remapping method, passed to regrid. Defaults to "bil". Methods available are:
        bilinear - "bil";
        nearest neighbour - "nn" - "nearest neighbour"
        bicubic interpolation - "bic"
        Distance-weighted average - "dis"
        First order conservative remapping - "con"
        Second order conservative remapping - "con2"
        Large area fraction remapping - "laf"

    Examples
    -------------

    Extract a 50 point transect across the North Atlantic:

    >>> ds.to_transect(start=[-70, 40], end=[-20, 55], nsteps=50)

    """

    valid_methods = ["bil", "nn", "bic", "dis", "con", "con2", "laf"]

    if method not in valid_methods:
        raise ValueError(f"{method} is not a valid method!")

    if start is None:
        raise ValueError("Please supply start")
    if end is None:
        raise ValueError("Please supply end")
    if nsteps is None:
        raise ValueError("Please supply nsteps")

    for name, point in [("start", start), ("end", end)]:
        if not isinstance(point, list):
            raise TypeError(f"{name} must be a list")
        if len(point) != 2:
            raise ValueError(f"{name} must be a 2 element [lon, lat] list")
        for x in point:
            if not isinstance(x, (int, float)):
                raise TypeError(f"{name} must contain only int or float values")

    if isinstance(nsteps, bool) or not isinstance(nsteps, (int, np.integer)):
        raise TypeError("nsteps must be an int")
    if nsteps < 2:
        raise ValueError("nsteps must be at least 2")

    lons = np.linspace(start[0], end[0], nsteps)
    lats = np.linspace(start[1], end[1], nsteps)

    transect_points = pd.DataFrame({"lon": lons, "lat": lats})

    self.regrid(grid=transect_points, method=method)
