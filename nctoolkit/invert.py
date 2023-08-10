
def invert(self, x = None):
    """
    invert: Invert levels or latitudes 

    Parameters
    -------------
    x: str
        What you want to invert. Either "levels" or "latitudes"
        Note: this is reasonably fuzzzy so anything with "lev" or "lat" will work

    """

    # create the cdo call and run it
    if "lev" in x.lower():
        cdo_command = "cdo invertlev" 
    
    elif "lat" in x.lower():
        cdo_command = "cdo invertlat"

    else:
        raise ValueError("x must be either levels or latitudes")

    self.cdo_command(cdo_command, ensemble=False)
