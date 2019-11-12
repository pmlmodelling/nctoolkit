import os
import xarray as xr
import pandas as pd
import subprocess
import sys
from .flatten import str_flatten
from ._generate_grid import generate_grid
from ._session import nc_safe
from ._cleanup import cleanup
from ._cleanup import clean_all
from ._cleanup import deep_clean 
from ._cleanup import temp_check 
from netCDF4 import Dataset
import copy

from ._temp_file import temp_file

import random
import string

from ._create_ensemble import create_ensemble 
from ._create_ensemble import generate_ensemble 

from ._show import nc_variables
from ._session import session_stamp
from ._session import session_info


letters = string.ascii_lowercase
session_stamp["stamp"] = "nchack" + "".join(random.choice(letters) for i in range(8)) + "nchack"
session_stamp["temp_dir"] = "/tmp/"
session_info["thread_safe"] = False 
session_info["lazy"] = False

import atexit
atexit.register(clean_all)

# run temp_check to see if any files are held over from previous sessions
temp_check()


result = os.statvfs("/tmp/")
session_info["size"] = result.f_frsize * result.f_bavail 
session_info["latest_size"] = 0 

def options(**kwargs):
    """
    Define session options.
    Set the options in the session. Available options are thread_safe and lazy.
    Set thread_safe = True if hdf5 was built to be thread safe.
    Set lazy = True if you want methods to evaluate lazy by default.

    Parameters
    ---------------
    **kwargs
        Define options using key, value pairs.

    """

    valid_keys = ["thread_safe", "lazy"] 
    for key in kwargs:
        if key not in valid_keys:
            raise AttributeError(key + " is not a valid option")
        if type(kwargs[key]) is not bool: 
            raise AttributeError("thread_safe must be True or False")
        else:
            session_info[key] = kwargs[key]






def convert_bytes(num):
    """
     A function to make file size human readable
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1000.0:
            return str(num) + " " + x 
        num /= 1000.0


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def open_data(x = None):

    """
    Read netcdf data as a DataSet object 

    Parameters
    ---------------

    x : str or list
        A string or list of netcdf files. The function will check the files exist

    """

    if x == None:
            raise ValueError("No data was supplied!")

    if (type(x) is str or type(x) is list) == False:
            raise ValueError("Please supply string or list!")

    if type(x) is str:
        if os.path.exists(x) == False:
            raise ValueError("Data set " + x + " does not exist!")
        else:
            nc_safe.append(x)


    # it's possible there are duplicates in the data
    # Get rid of them..

    if type(x) is list:
        orig_size = len(x)
        x = list(set(x))
        if len(x) < orig_size:
            print("Warning: duplicates in data set have been removed!")

    if type(x) is list:
        for ff in x:
            if os.path.exists(ff) == False:
                raise ValueError("Data set " + ff + " does not exist!")
            else:
                nc_safe.append(ff)

    # if there is only one file in the list, change it to a single file
    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    return DataSet(x)
    
def merge(*trackers, match = ["year", "month", "day"]):
    all_files = []
    for tracker in trackers:
        if "DataSet" in str(type(tracker)) == False:
            raise ValueError("Please check everything is an DataSet object!")
        if type(tracker.current) is str:
            all_files += [tracker.current]
        else:
            all_files += tracker.current
    result = open_data(all_files)
    result.merge(match = match)
    return result

class DataSet(object):
    """A tracker/log for manipulating netcdf files"""
    def __init__(self, start = ""):
        """Initialize the starting file name etc"""
        self.history = []
        self.start = start
        self.current = start
        self.weights = None 
        self.grid = None 
        if session_info["lazy"]:
            self.run = False
        else:
            self.run = True
        self.hold_history = []
        self.merged = False
        self.released = False

    def __repr__(self):
        # tidy up the output first
        if isinstance(self.start,list):
            if len(self.start) > 10:
                start = ">10 ensemble member"
                start = str(len(self.start)) + " member ensemble"
            else:
                start = str_flatten(self.start)
        if type(self.start) == str:
            start = self.start

        if isinstance(self.current,list):
            if len(self.current) > 10:
                current = str(len(self.current)) + " member ensemble"
            else:
                current = str_flatten(self.current)
        if type(self.current) == str:
            current = self.current

        return "<nchack.DataSet>:\nstart: " + start + "\ncurrent: " + current + "\noperations: " + str(len(self.history))


    @property
    def size(self):
        """The size of an object 
        This will print the number of files, total size, and smallest and largest files in an DataSet object.
        """
        if type(self.current) is str:
            result = "Number of files: 1\n"
            result = result + "File size: " + convert_bytes(file_size(self.current))
            print(result)
        else:
            all_sizes = []
            
            smallest_file = ""
            largest_file = ""
            min_size = 1e15 
            max_size = -1 

            for ff in self.current:

                all_sizes.append(file_size(ff))

                if file_size(ff) > max_size:
                    max_size = file_size(ff)
                    largest_file = ff

                if file_size(ff) < min_size:
                    min_size = file_size(ff)
                    smallest_file = ff

            min_size = convert_bytes(min_size)
            max_size = convert_bytes(max_size)

            sum_size = convert_bytes(sum(all_sizes))
            result = "Number of files in ensemble: " + str(len(self.current)) + "\n"
            result = result + "Ensemble size: " + sum_size  + "\n"
            result = result + "Smallest file " + smallest_file + " has size "  + min_size  + "\n"
            result = result + "Largest file " + largest_file + " has size "  + max_size 
            print(result)

    @property
    def variables(self):
        """
        Variables contained in an object's netcdf file.
        This will check the netcfile's contents, if it is a single file DataSet object.
        """
        
        if type(self.current) is list:
            print("This DataSet object is a list. Please inspect individual files using nc_variables")
  
        cdo_result = subprocess.run("cdo showname " + self.current, shell = True, capture_output = True)
        cdo_result = str(cdo_result.stdout).replace("b'", "").replace("\\n", "").replace("'", "").strip()
        cdo_result = cdo_result.split()
  
        return(cdo_result)

    @property
    def variables_detailed(self):
        """
        Variables contained in an object's netcdf file.
        This will check the netcfile's contents, if it is a single file DataSet object.
        """
        
        if type(self.current) is list:
            print("This DataSet object is a list. Please inspect individual files using nc_variables")
  
        cdo_result = subprocess.run("cdo showname " + self.current, shell = True, capture_output = True)
        cdo_result = str(cdo_result.stdout).replace("b'", "").replace("\\n", "").replace("'", "").strip()
        cdo_result = cdo_result.split()
        dataset = Dataset(self.current)

        longs = None
        units = None
        if "long_name" in str(dataset.variables[cdo_result[0]]):
                longs = [dataset.variables[x].long_name for x in cdo_result]
        if "units" in str(dataset.variables[cdo_result[0]]):
                longs = [dataset.variables[x].units for x in cdo_result]

        if longs is None and units is None:
            return(cdo_result)

        df = pd.DataFrame({"variable": cdo_result})
        if longs is not None:
            df["long_name"] = longs
        if units is not None:
            df["units"] = units
        return df
            

    @property
    def start(self):
        """
        The starting file or files of the DataSet object
        """
        return self._start

    @start.setter
    def start(self, value):
        if type(value) is str:
            self._start = value
        if isinstance(value,list):
            self._start = value

    @property
    def current(self):
        """
        The current file or files in the DataSet object
        """
        return self._current

    @current.setter
    def current(self, value):
        if type(value) is str:
            self._current = value
        if isinstance(value,list):
            self._current = value

    @property
    def history(self):
        """
        The history of operations on the DataSet 
        """
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def run(self):
        """
        Is the object in run or lazy eval mode? 
        """
        return self._run

    @run.setter
    def run(self, value):
        self._run = value

    def lazy(self):
        """
        Set the method evaluation mode to lazy 
        """
        self.run = False 
        self.hold_history = copy.deepcopy(self.history)

    def copy(self):
        """
        Make a deep copy of an DataSet object
        """
        new = copy.deepcopy(self)
        if type(new.current) is str:
            nc_safe.append(new.current)
        else:
            for ff in new.current:
                nc_safe.append(ff)
        return new

    def str_flatten(L, sep = ","):
        result = sep.join(str(x) for x in L)
        return(result)
    def __del__(self):
        if type(self.current) is str:
            if self.current in nc_safe:
                nc_safe.remove(self.current)
        else:
            for ff in self.current:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")
 
    from ._toxarray import to_xarray
    from ._cellareas import cell_areas
    from ._regrid import regrid

    from ._ensembles import ensemble_mean
    from ._ensembles import ensemble_mean_cdo
    from ._ensembles import ensemble_max
    from ._ensembles import ensemble_min
    from ._ensembles import ensemble_range
    from ._ensembles import ensemble_percentile

    from ._clip import clip
    from ._select import select_variables
    from ._select import select_timestep

    from ._cdo_command import cdo_command

    from ._expr import mutate 
    from ._expr import transmute 

    from ._select import select_season
    from ._select import select_months
    from ._select import select_years

    from ._seasstat import seasonal_mean 
    from ._seasstat import seasonal_min
    from ._seasstat import seasonal_max 
    from ._seasstat import seasonal_range

    from ._seasclim import seasonal_mean_climatology
    from ._seasclim import seasonal_min_climatology
    from ._seasclim import seasonal_max_climatology
    from ._seasclim import seasonal_range_climatology

    from ._yearlystat import annual_mean 
    from ._yearlystat import annual_min
    from ._yearlystat import annual_max 
    from ._yearlystat import annual_range

    from ._monstat import monthly_mean
    from ._monstat import monthly_min
    from ._monstat import monthly_max
    from ._monstat import monthly_range

    from ._monthlyclim import monthly_mean_climatology
    from ._monthlyclim import monthly_min_climatology
    from ._monthlyclim import monthly_max_climatology
    from ._monthlyclim import monthly_range_climatology

    from ._dailyclim import daily_mean_climatology
    from ._dailyclim import daily_min_climatology
    from ._dailyclim import daily_max_climatology
    from ._dailyclim import daily_range_climatology

    from ._to_nc import write_nc 

    from ._rename import rename 

    from ._setters import set_date 
    from ._setters import set_missing
    from ._setters import set_units
    from ._setters import set_longnames
    from ._setters import set_gridtype
    from ._setters import set_attributes
    from ._setters import assign_coords


    from ._time_stat import mean 
    from ._time_stat import percentile
    from ._time_stat import max
    from ._time_stat import min
    from ._time_stat import range
    from ._time_stat import var
    from ._time_stat import sum
    from ._time_stat import cum_sum
    #from ._time_stat import percentile 

    from ._release import release 

    from ._delete import remove_variables

    from ._mergers import merge_time 
    from ._mergers import merge

    from ._rollstat import rolling_mean
    from ._rollstat import rolling_min
    from ._rollstat import rolling_max
    from ._rollstat import rolling_range
    from ._rollstat import rolling_sum

    from ._show import times
    from ._show import years 
    from ._show import months
    from ._show import levels

    from ._fldstat import spatial_mean
    from ._fldstat import spatial_min
    from ._fldstat import spatial_max
    from ._fldstat import spatial_range
    from ._fldstat import spatial_sum

    from ._verticals import vertical_mean 
    from ._verticals import vertical_min
    from ._verticals import vertical_max
    from ._verticals import vertical_range
    from ._verticals import surface
    from ._verticals import vertical_interp
    from ._verticals import bottom 

    from ._view import view

    from ._zip import zip

    from ._checkers import check_dates
    from ._checkers import ensemble_check
    
    from ._corr import cor_space
    from ._corr import cor_time

    from ._phenology import phenology

    from ._split import split

    from ._anomaly import annual_anomaly

    from ._masking import mask_lonlat

    from ._inttime import time_interp

    from ._cleanup import disk_clean 

    from ._time_sort import sort_times
    from ._safe import safe_list
    
    from._plot import autoplot

    from._twofiles import multiply



