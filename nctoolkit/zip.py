from nctoolkit.runthis import run_this


def zip(self):
    """
    Zip the dataset
    This will compress the files within the dataset. This works lazily.
    """
    self._zip = True
