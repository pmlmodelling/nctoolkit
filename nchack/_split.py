import os
import glob
import copy
import multiprocessing

from ._temp_file import temp_file
from ._filetracker import nc_created
from .flatten import str_flatten
from ._select import select_variables
from ._setters import set_longname
import copy


def split(self, method = "year", silent = False):
    """
    Method to split files by year 
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
        split_base = temp_file() 
    
        cdo_command = "cdo split" + method + " "  + ff +  " " + split_base
    
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
                counter+=1

        if counter == 0:
            raise ValueError("Splitting the file by year did not work!")


    self.current = new_files



def split_year(self,  silent = False):
    split(self, method = "year", silent = silent)

def split_year_month(self,  silent = False):
    split(self, method = "yearmon", silent = silent)

def split_month(self,  silent = False):
    split(self, method = "mon", silent = silent)

def split_day(self,  silent = False):
    split(self, method = "day", silent = silent)

def split_season(self,  silent = False):
    split(self, method = "seas", silent = silent)


