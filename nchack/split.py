import os
import glob
import copy
import multiprocessing

from .temp_file import temp_file
from .session import nc_safe
from .flatten import str_flatten
from .select import select_variables
from .setters import set_longnames
from .session import session_stamp
from .session import session_info

import copy


def split_cdo(self, method = "year"):
    """
    Method to split files by period
    """
    self.release()

    if type(self.current) is str:
        ff_list = [self.current]
    else:
        ff_list = self.current

    new_files = []
    for ff in ff_list:

        # We need to split the file by name

        # But, first we need to check whether there is sufficient space in the output folder
        # If there isn't, we need to switch to the /var/tmp

        if session_stamp["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail
            session_info["size"] = result

            if os.path.getsize(ff)*2 > session_info["size"]:
                    session_stamp["temp_dir"] = "/var/tmp/"

        split_base = temp_file()

        cdo_command = "cdo -s -split" + method + " "  + ff +  " " + split_base

        os.system(cdo_command)

        self.history.append(cdo_command)
        self._hold_history = copy.deepcopy(self.history)

        # now, pull out the files generated

        mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
        mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
        mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]

        counter = 0
        for x in mylist:
            if split_base in x:
                new_files.append(x)
                nc_safe.append(x)
                counter+=1

        if counter == 0:
            raise ValueError("Splitting the file by year did not work!")

    self.merged = False
    self.current = new_files


def split(self, by = None):
    """
    Split the ensemble
    Each file in the ensemble will be separated into new files based on the splitting argument.

    Parameters
    --------------------
    by : int
        Available by arguments are 'year', 'month', 'yearmonth', 'season', 'day'
    """

    if by == "year":
        method = "year"

    if by == "yearmonth":
        method = "yearmon"

    if by == "season":
        method = "seas"

    if by == "day":
        method = "day"

    split_cdo(self, method = method)



