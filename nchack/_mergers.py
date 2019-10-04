
from ._cleanup import cleanup
from ._runthis import run_this

def merge(self, silent = True):
    """Method to merge a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    if self.run == False:
        if (len(self.current) * (len(self.history) - len(self.hold_history))) > 127:
            raise ValueError("You cannot chain more than 128 operations!")

    cdo_command = ("cdo merge")


    run_this(cdo_command, self, silent, output = "one") 

    self.release()


    # clean up the directory
    cleanup(keep = self.current)


def merge_time(self, silent = True):
    """Method to to a time-based merge of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    if self.run == False:
        if (len(self.current) * (len(self.history) - len(self.hold_history))) > 127:
            raise ValueError("You cannot chain more than 128 operations!")

    cdo_command = "cdo mergetime"

    run_this(cdo_command, self, silent, output = "one") 

    self.release()

    # clean up the directory
    cleanup(keep = self.current)
