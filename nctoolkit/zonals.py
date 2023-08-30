from nctoolkit.utils import is_curvilinear
from nctoolkit.api import open_data


def zonstat(self, stat="mean"):
    """Method to calculate the zonal statistic from a netCDF file"""

    for ff in self:
        if is_curvilinear(ff):
            raise TypeError(f"zonal_{stat} cannot be calculated for curvilinear grids.")

    cdo_command = f"-zon{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def zonal_sum(self, by_area=False):
    """
    zonal_sum: Calculate the zonal sum for each time step

    Parameters
    -------------
    by_area : bool
        Set to True if you want the cell value to be multiplied by the cell area prior to summing

    Examples
    ------------
    If you want to calculate the zonal sum for a dataset, do the following:

    >>> ds.zonal_sum()

    """
    if by_area is True:
        if len(self) > 1:
            print("Using first file in the dataset for areas")
        ds_area = open_data(self[0])
        ds_area.subset(time=0)
        ds_area.cell_area(join=False)
        self.multiply(ds_area)

    zonstat(self, stat="sum")


def zonal_mean(self):
    """
    zonal_mean: Calculate the zonal mean for each time step

    Examples
    ------------
    If you want to calculate the zonal mean for a dataset, do the following:

    >>> ds.zonal_mean()

    """
    zonstat(self, stat="mean")


def zonal_min(self):
    """
    zonal_min: Calculate the zonal minimum for each time step

    Examples
    ------------
    If you want to calculate the zonal minimum for a dataset, do the following:

    >>> ds.zonal_min()
    """
    zonstat(self, stat="min")


def zonal_max(self):
    """
    zonal_max: Calculate the zonal maximum for each time step

    Examples
    ------------
    If you want to calculate the zonal maximum for a dataset, do the following:

    >>> ds.zonal_max()
    """
    zonstat(self, stat="max")


def zonal_range(self):
    """
    zonal_range: Calculate the zonal range for each time step

    Examples
    ------------
    If you want to calculate the zonal range for a dataset, do the following:

    >>> ds.zonal_range()

    """
    zonstat(self, stat="range")
