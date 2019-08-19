import os
import xarray as xr
import sys
import tempfile
from .flatten import str_flatten
from ._generate_grid import generate_grid
from ._filetracker import nc_created
from ._cleanup import cleanup
import copy
from ._create_ensemble import create_ensemble 

class NCTracker:
    """A tracker/log for manipulating netcdf files"""
    def __init__(self, start = ""):
        """Initialize the starting file name etc"""
        self.history = []
        self.start = start
        self.current = start
        self.weights = None 
        self.grid = None 
        self.target = None

    def __repr__(self):
        # tidy up the output first
        if isinstance(self.start,list):
            if len(self.start) > 10:
                start = ">10 ensemble member"
            else:
                start = str_flatten(self.start)
        if type(self.start) == str:
            start = self.start

        if isinstance(self.current,list):
            if len(self.current) > 10:
                current = ">10 ensemble member"
            else:
                current = str_flatten(self.current)
        if type(self.current) == str:
            current = self.current

        return "<nchack.NCTracker>:\nstart: " + start + "\ncurrent: " + current + "\noperations: " + str(len(self.history))


    # todo
    # make it impossible to delete the start point
    
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, value):
        if type(value) is str:
            if value == "":
                self._start = value
            else:
                if os.path.exists(value):
                    self._start = value
                else:
                    raise TypeError("File does not exist")
        if isinstance(value,list):
            self._start = value

    def append(self, x):
        """A function for creating a new tracker using an existing one as the starting point"""
        
        # 1st, current needs to be convert to a list if we are able to append something to it
        if type(self.current) is str:
            self.current = [self.current]
        if type(x) is str:
            self.current.append(x)
        else:
            self.current = self.current + x
        return(self)

    def update(self, current):
        """A function for creating a new tracker using an existing one as the starting point"""
        self.current = current
        if self.start == "":
            self.start = current
        return(self)

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
        new.target = None
        return(new)


    def str_flatten(L, sep = ","):
        result = sep.join(str(x) for x in L)
        return(result)
    def __del__(self):
        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")
 
    from ._variables import variables
    from ._toxarray import to_xarray
    from ._cellareas import cell_areas
    from ._regrid import regrid
    from ._surface import surface
    from ._vertint import vertical_interp
    from ._ensmean import ensemble_mean
    from ._ensmax import ensemble_max
    from ._ensmin import ensemble_min
    from ._ensrange import ensemble_range
    from ._clip import clip
    from ._selname import select_variables
    from ._cdo_command import cdo_command
    from ._mutate import mutate 
    from ._transmute import transmute
    from ._times import times
    from ._ensemble_check import ensemble_check
    from ._mean import mean 
    from ._set_missing import set_missing
    from ._select_season import select_season
    from ._ensemble_percentile import ensemble_percentile
    from ._vertstat import vertical_mean 
    from ._vertstat import vertical_min
    from ._vertstat import vertical_max
    from ._vertstat import vertical_range

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

    from ._to_nc import to_netcdf

    from ._rename import rename 
    from ._set_date import set_date 


