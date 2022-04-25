


def validator():

    val = Validator()
    return val





class Validator(object):
    """
    A modifiable ensemble of netCDF files
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.model = None
        self.obs = None
        self.plots = []


    # Import any methods

    from nctoolkit.validator_funs import add_observations
    from nctoolkit.validator_funs import add_model
    from nctoolkit.validator_funs import matchup
    from nctoolkit.validator_funs import validate
