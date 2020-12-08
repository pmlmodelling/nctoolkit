from nctoolkit.runthis import run_this
from nctoolkit.session import session_info


def zip(self):
    """
    Zip the dataset
    This will compress the files within the dataset. This works lazily.
    """
    self._zip = True
    if session_info["lazy"] == False:
        self._execute = False
        self.run()
