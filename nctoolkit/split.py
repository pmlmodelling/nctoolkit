import glob
import copy
import os
import platform

from nctoolkit.cleanup import cleanup
from nctoolkit.temp_file import temp_file
from nctoolkit.session import session_info, temp_dirs, temp_files


def split_cdo(self, method="year"):
    """
    Method to split files by period
    """
    # this cannot me chained. So release
    self.run()

    new_files = []

    commands = []

    for ff in self:

        # We need to split the file by name
        # But, first we need to check if there is space in the output folder
        # If there isn't, we need to switch to the /var/tmp

        if platform.system() == "Linux":
            if session_info["temp_dir"] == "/tmp/":
                result = os.statvfs("/tmp/")
                result = result.f_frsize * result.f_bavail
                session_info["size"] = result

                if os.path.getsize(ff) * 2 > session_info["size"]:
                    session_info["temp_dir"] = "/var/tmp/"

        split_base = temp_file()

        cdo_command = f"cdo -s -split{method} {ff} {split_base}"

        os.system(cdo_command)

        commands.append(cdo_command)

        # now, pull out the files generated

        counter = 0
        for directory in temp_dirs:
            mylist = [f for f in glob.glob(f"{directory}/*.nc*")]
            mylist = [f for f in mylist if session_info["stamp"] in f]
            for ff in mylist:
                if split_base in ff:
                    new_files.append(ff)
                    temp_files.add(ff)
                    counter += 1

        if counter == 0:
            raise ValueError("Splitting the file did not work!")

    self.history += commands
    self._hold_history = copy.deepcopy(self.history)

    self._merged = False
    self.current = new_files

    cleanup()
    self.disk_clean()


def split(self, by=None):
    """
    Split the dataset
    Each file in the ensemble will be separated into new files based on the
    splitting argument.

    Parameters
    --------------------
    by : str
        Available by arguments are 'year', 'month', 'yearmonth', 'season', 'day'.
        year will split files by year, month will split files by month, yearmonth
        will split files by year and month; season will split files by year, day
        will split files by day.
    """

    if by is None:
        raise ValueError("No valid split method supplied")

    method = None
    if by == "year":
        method = "year"

    if by == "month":
        method = "mon"

    if by == "yearmonth":
        method = "yearmon"

    if by == "season":
        method = "seas"

    if by == "day":
        method = "day"

    if method is None:
        raise ValueError("No valid split method supplied")

    split_cdo(self, method=method)
