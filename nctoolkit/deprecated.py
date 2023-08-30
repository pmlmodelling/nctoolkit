
import warnings

def invert_levels(self):
    """
    Invert the levels of 3D variables.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to invert the vertical levels, you would do this:

    >>> ds.invert_levels()

    """
    # add deprecation warning message
    warnings.warn(
        "invert_levels is deprecated and will be removed in a future version. Please use invert instead",
        DeprecationWarning,
    )
    cdo_command = "-invertlev"

    self.cdo_command(cdo_command, ensemble=False)

