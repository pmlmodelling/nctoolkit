
from ._cleanup import cleanup
from ._runthis import run_this

def merge(self, silent = True):
    """Method to merge a list of files"""


    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    self.merged = True
    if "merge " in self.history or "mergetime " in self.history:
        raise ValueError("You cannot double chain merge methods!")

    # add a check for the number of operations 
    if self.run == False:
        if (len(self.current) * (len(self.history) - len(self.hold_history))) > 127:
            raise ValueError("You cannot chain more than 128 operations in CDO. Consider releasing the tracker prior to merging!")

    cdo_command = ("cdo -merge ")

    self.history.append(cdo_command)

    if self.run:
        run_this(cdo_command, self, silent, output = "one") 
    else:
        self.release(run_merge = False)

    # clean up the directory
    cleanup(keep = self.current)


def merge_time(self, silent = True):
    """Method to to a time-based merge of files"""

    if "merge " in self.history or "mergetime " in self.history:
        raise ValueError("You cannot double chain merge methods!")

    self.merged = True
    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo -mergetime "

    self.history.append(cdo_command)

    if self.run:
        run_this(cdo_command, self, silent, output = "one") 
    else:
        self.release(run_merge = False)


    # clean up the directory
    cleanup(keep = self.current)



