from nctoolkit.runthis import run_this
from nctoolkit.utils import is_curvilinear
import subprocess


def centre(self, by ="latitude", by_area = False):
    """
    Calculate the latitudinal or longitudinal centre for each year/month combination in files.
    This applies to each file in an ensemble.
    by : str
        Set to 'latitude' if you want the latitiduinal centre calculated. 'longitude' for longitudinal.
    by_area : bool
        If the variable is a value/m2 type variable, set to True, otherwise set to False.
    """

    if by not in ["longitude", "latitude"]:
        raise ValueError("by is not valid. Please check!")

    if type(by_area) is not bool:
        raise TypeError("by_area is not boolean. Please check!")

    self.run()

    if type(self.current) is list:
        raise TypeError("This method still does not work with lists! Consider merging.")

    data1 = self.copy()
    ops = dict()
    for var in self.variables:
        if by == "latitude":
            ops[var] = (f"{var}*clat({var})")
        else:
            ops[var] = (f"{var}*clon({var})")

    self.transmute(ops)
    data1.spatial_sum(by_area = by_area)
    self.spatial_sum(by_area = by_area)
    self.divide(data1)








