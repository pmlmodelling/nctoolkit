
def centre(self, by="latitude", by_area=False):
    """
    Calculate the latitudinal or longitudinal centre for each year/month combination in files.
    This applies to each file in an ensemble.

    Parameters
    -------------
    by : str
        Set to 'latitude' if you want the latitiduinal centre calculated. 'longitude' for longitudinal.
    by_area : bool
        If the variable is a value/m2 type variable, set to True, otherwise set to False.
    """

    if by not in ["longitude", "latitude"]:
        raise ValueError("by is not valid. Please check!")

    if not isinstance(by_area, bool):
        raise TypeError("by_area is not boolean. Please check!")

    self.run()

    if len(self) > 1:
        raise TypeError("This method still does not work with lists! Consider merging.")

    ds1 = self.copy()
    ops = []
    for var in self.variables:
        if by == "latitude":
            ops.append(f"{var}={var}*clat({var})")
        else:
            ops.append(f"{var}={var}*clon({var})")

    ops = ";".join(ops)
    ops = f"expr,'{ops}'"
    self.cdo_command(ops)
    ds1.spatial_sum(by_area=by_area)
    self.spatial_sum(by_area=by_area)
    self.divide(ds1)
