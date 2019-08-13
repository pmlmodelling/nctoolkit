import os
import xarray as xr
import sys
import tempfile
from .flatten import str_flatten
from ._generate_grid import generate_grid
from ._filetracker import nc_created
from ._cleanup import cleanup
import copy

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
        if isinstance(self.start,list):
            if len(self.start) > 10:
                return "<nchack.NCTracker>:\nstart: " + ">10 member ensemble" + "\ncurrent: " + ">10 member ensemble" + "\noperations: " + str(len(self.history))
            else:
                return "<nchack.NCTracker>:\nstart: " + str_flatten(self.start) + "\ncurrent: " + str_flatten(self.current) + "\noperations: " + str(len(self.history))
        else:
            if self.start is None:
                return "<nchack.NCTracker>:\nstart: "+ str(self.start) + "\ncurrent: " + str(self.current) + "\noperations: " + str(len(self.history))
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
            if value == "":
                self._start = value
            else:
                if os.path.exists(value):
                    self._start = value
                else:
                    raise TypeError("File does not exist")
        if isinstance(value,list):
            self._start = value


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
##        print("deleted")
        cleanup()

#    def __del__(self):
#        if isinstance(self.start,list):
#            if isinstance(self.current, list) == False:
#                if os.path.exists(self.current):
#                    os.remove(self.current)
#        else: 
#            if self.current != self.start:
#                if os.path.exists(self.current):
#                    os.remove(self.current)
#
#                if self.grid is not None or self.weights is not None:
#                # We do not want to delete the weights and grid if they are in use by another tracker
#                    valid_grid = 0 
#                    valid_weights = 0 
#                    objects = dir(sys.modules["__main__"])
#                    for i in ([v for v in objects if not v.startswith('_')]):
#                        i_class = str(eval("type(sys.modules['__main__']." +i + ")"))
#                        if "NCTracker" in i_class:
#                            i_grid = eval("sys.modules['__main__']." +i + ".grid")
#                            i_weights = eval("sys.modules['__main__']." +i + ".weights")
#                            if self.grid is not None:
#                                valid_grid += i_grid == self.grid
#                    
#                            if self.weights is not None:
#                                valid_weights += i_weights == self.weights
#                    if valid_weights == 0 and os.path.exists(self.weights):
#                        os.remove(self.weights)
#
#                    if valid_grid == 0 and os.path.exists(self.grid):
#                        os.remove(self.grid)
#                    


                               ## del self

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")
 
    from ._variables import variables
    from ._toxarray import to_xarray
    from ._cellareas import cellareas
    from ._expr import expr
    from ._regrid import regrid
    from ._surface import surface
    from ._vertint import vertint
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



#class NCTrackerList:
#    def __init__(self, start):
#        """Initialize the starting file name etc"""
#        self.ensemble = [start]
#        cleanup(keep = start)
#
#    def add(self, new):
#        """A function for adding a new variable to an ensemble"""
#        self.ensemble.append(new.current)
#        cleanup(keep = new.current)
#        return(self)
#
#
#    def __del__(self):
#        print("deleted")
#        cleanup()
#
