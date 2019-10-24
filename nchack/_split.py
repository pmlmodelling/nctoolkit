import os
import glob
import copy
import multiprocessing

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
from ._session import session_stamp
from ._session import session_info

import copy


def split(self, method = "year"):
    """
    Method to split files by period 
    """
    if self.run == False:
        raise ValueError("This cannot be run with held over commands. Please release commands prior to running")

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
#        print(split_base)
    
        cdo_command = "cdo -s -split" + method + " "  + ff +  " " + split_base
    
        self.history.append(cdo_command)
    
        os.system(cdo_command)

        # now, pull out the files generated

        mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
        mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
        mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]

        counter = 0
        for x in mylist:
            if split_base in x:
                new_files.append(x)
                nc_created.append(x)
                counter+=1

        if counter == 0:
            raise ValueError("Splitting the file by year did not work!")

        

    self.merged = False
    self.current = new_files



def split_year(self):
    """
    Split the ensemble based on years. Each file in the ensemble will be separated into new files based on years.

    Returns
    -------------
    nchack.NCData
        Reduced tracker with split data
    """
    split(self, method = "year")

def split_year_month(self):
    """
    Split the ensemble based on years and months. Each file in the ensemble will be separated into new files based on years and months.

    Returns
    -------------
    nchack.NCData
        Reduced tracker with split data
    """
    split(self, method = "yearmon")

#def split_month(self):
#    split(self, method = "mon")

def split_day(self):
    """
    Split the ensemble based on days. Each file in the ensemble will be separated into new files based on days.

    Returns
    -------------
    nchack.NCData
        Reduced tracker with split data
    """
    split(self, method = "day")

def split_season(self):
    """
    Split the ensemble based on season. Each file in the ensemble will be separated into new files based on season.

    Returns
    -------------
    nchack.NCData
        Reduced tracker with split data
    """
    split(self, method = "seas")


