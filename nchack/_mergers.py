
from ._cleanup import cleanup
from ._runthis import run_this

def merge(self, silent = True):
    """Method to merge a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    if len(self.hold_history) > 0:
        raise ValueError("You cannot run merge_time with pre-existing hold over commands!")

    cdo_command = ("cdo merge")

    run_this(cdo_command, self, silent, output = "one") 

    # clean up the directory
    cleanup(keep = self.current)


def merge_time(self, silent = True):
    """Method to to a time-based merge of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    if len(self.hold_history) > 0:
        raise ValueError("You cannot run merge_time with pre-existing hold over commands!")

    cdo_command = "cdo mergetime"

    run_this(cdo_command, self, silent, output = "one") 

    # clean up the directory
    cleanup(keep = self.current)
