import os
import xarray as xr
import sys
import tempfile
from .flatten import str_flatten
from ._generate_grid import generate_grid
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._cleanup import clean_all
from ._cleanup import deep_clean 
from ._cleanup import temp_check 
import copy
from ._create_ensemble import create_ensemble 
from ._create_ensemble import generate_ensemble 

from ._show import nc_variables
print("Tip: include atexit.register(nchack.clean_all) after loading nchack")
temp_check()


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



class NCTracker:
    """A tracker/log for manipulating netcdf files"""
    def __init__(self, start = ""):
        """Initialize the starting file name etc"""
        self.history = []
        self.start = start
        self.current = start
        self.weights = None 
        self.grid = None 
        self.run = True
        self.hold_history = []
        self.merged = False

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

        return "<nchack.NCTracker>:\nstart: " + start + "\ncurrent: " + current + "\noperations: " + str(len(self.history))


    @property
    def size(self):

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
        if type(self.current) is list:
            print("This tracker is a list. Please inspect individual files using nc_variables")
  
        cdo_result = os.popen( "cdo showname " + self.current).read()
        cdo_result = cdo_result.replace("\n", "")
        cdo_result = cdo_result.split()
  
        print(cdo_result)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if type(value) is str:
            self._start = value
            if value == "":
                self._start = value
            else:
                if os.path.exists(value):
                    self._start = value
                else:
                    raise TypeError("File does not exist")
        if isinstance(value,list):
            self._start = value

    def hold(self):
        """A method to set the mode to hold"""
        self.run = False 
        self.hold_history = copy.deepcopy(self.history)
        
    def lazy(self):
        """A method to set the mode to lazy"""
        self.run = False 
        self.hold_history = copy.deepcopy(self.history)


    def append(self, x):
        """A function for creating a new tracker using an existing one as the starting point"""
        
        # 1st, current needs to be convert to a list if we are able to append something to it
        if type(self.current) is str:
            self.current = [self.current]
        if type(x) is str:
            self.current.append(x)
        else:
            self.current = self.current + x

    def restart(self, start = None):
        """A function for creating a new tracker using an existing one as the starting point"""
        new = copy.copy(self)
        new.history = []
        if start is None:
            new.start = self.current
            new.current = new.start
        else:
            new.start = start
            new.current = start
        return(new)


    def str_flatten(L, sep = ","):
        result = sep.join(str(x) for x in L)
        return(result)
    def __del__(self):
        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")
 
    from ._toxarray import to_xarray
    from ._cellareas import cell_areas
    from ._regrid import regrid

    from ._ensembles import ensemble_mean
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

    from ._yearlystat import yearly_mean 
    from ._yearlystat import yearly_min
    from ._yearlystat import yearly_max 
    from ._yearlystat import yearly_range

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

    from ._to_nc import to_netcdf

    from ._rename import rename 

    from ._setters import set_date 
    from ._setters import set_missing
    from ._setters import set_unit 
    from ._setters import set_longname

    from ._time_stat import mean 
    from ._time_stat import max
    from ._time_stat import min
    from ._time_stat import range
    from ._time_stat import var
    from ._time_stat import sum
    from ._time_stat import cum_sum
    #from ._time_stat import percentile 

    from ._release import release 

    from ._delete import remove_variable 

    from ._mergers import merge_time 
    from ._mergers import merge

    from ._rollstat import rolling_mean
    from ._rollstat import rolling_min
    from ._rollstat import rolling_max
    from ._rollstat import rolling_range
    from ._rollstat import rolling_sum

    from ._ncks_command import ncks_command 

    from ._show import times
    from ._show import numbers 
    from ._show import show_years 
    from ._show import show_months
    from ._show import show_levels
    from ._show import depths

    from ._fldstat import spatial_mean
    from ._fldstat import spatial_min
    from ._fldstat import spatial_max
    from ._fldstat import spatial_range

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

    from ._split import split_year
    from ._split import split_year_month




