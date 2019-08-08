import os
import xarray as xr
import tempfile
from .flatten import str_flatten
from ._generate_grid import generate_grid
from ._variables import variables
from ._filetracker import nc_created
from ._cleanup import cleanup
import copy

class NCTracker:
    """A tracker/log for manipulating netcdf files"""
    def __init__(self, start):
        """Initialize the starting file name etc"""
        self.history = []
        self.start = start
        self.current = start
        self.target = None

    def __repr__(self):
        if isinstance(self.start,list):
            if len(self.start) > 10:
                return "<nchack.NCTracker>:\nstart: " + ">10 member ensemble" + "\ncurrent: " + ">10 member ensemble" + "\noperations: " + str(len(self.history))
            else:
                return "<nchack.NCTracker>:\nstart: " + str_flatten(self.start) + "\ncurrent: " + str_flatten(self.current) + "\noperations: " + str(len(self.history))
        else:
            return "<nchack.NCTracker>:\nstart: "+self.start + "\ncurrent: " + self.current + "\noperations: " + str(len(self.history))


    # todo
    # make it impossible to delete the start point
    
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, value):
        if type(value) is str:
            if os.path.exists(value):
                self._start = value
            else:
                raise TypeError("File does not exist")
        if isinstance(value,list):
            self._start = value


    def restart(self):
        """A function for creating a new tracker using an existing one as the starting point"""
        return NCTracker(self.current)
       # new = copy.copy(self)
       # new.history = []
       # new.start = self.current
       # new.current = new.start
       # new.target = None
       # return(new)


    def str_flatten(L, sep = ","):
        result = sep.join(str(x) for x in L)
        return(result)

    def __del__(self):
        if isinstance(self.start,list):
            if isinstance(self.current, list) == False:
                if os.path.exists(self.current):
                    os.remove(self.current)
        else: 
            if self.current != self.start:
                if os.path.exists(self.current):
                    os.remove(self.current)
            del self

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")


    def del_current(self):
        if self.current != self.start:
            os.remove(self.current)
        if self.current == self.start:
            print("Current file is the same as the start file. Not deleted!")

 
    from ._toxarray import to_xarray
    from ._cellareas import cellareas
    from ._expr import expr
    from ._remap import regrid
    from ._surface import surface
    from ._vertint import vertint
    from ._ensmean import ensemble_mean
    from ._ensmax import ensemble_max
    from ._ensmin import ensemble_min
    from ._ensrange import ensemble_range
    from ._clip import clip
    from ._selname import select_variables

