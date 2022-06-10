

def open_matchpoint():

    return Matchpoint()


class Matchpoint(object):
    """
    A modifiable ensemble of netCDF files
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        self.data = None
        self.points = None
        self.temporal = True
        self.depths = None
        self.variables = None
        self.top = True
        self.values = None
        self.max_extrap = 5

    # Import any methods

    from nctoolkit.mp_adders import add_data
    from nctoolkit.mp_adders import add_points
    from nctoolkit.mp_adders import add_depths
    from nctoolkit.mp_matchups import matchup
