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
    # todo
    # make it impossible to delete the start point

    def restart(self):
        new = copy.copy(self)
        new.history = []
        new.start = self.current
        new.current = new.start
        new.target = None
        return(new)


    def str_flatten(L, sep = ","):
        result = sep.join(str(x) for x in L)
        return(result)
    
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, value):
        if os.path.exists(value):
            self._start = value
        else:
            raise TypeError("File does not exist")
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
    from ._remap import remap
    from ._surface import surface
    from ._vertint import vertint
    from ._clip import clip

