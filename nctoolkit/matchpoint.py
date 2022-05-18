

def open_matchpoint():

    val = Matcher()
    return val


class Matcher(object):
    """
    A modifiable ensemble of netCDF files
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.model = None
        self.obs = None
        self.variable = None
        self.cores = 1
        self.top = True


    # Import any methods

    from nctoolkit.mp_adders import add_depths
    from nctoolkit.mp_adders import add_model
    from nctoolkit.mp_adders import add_observations
    from nctoolkit.mp_matchups import matchup
