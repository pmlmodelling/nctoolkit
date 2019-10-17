import os

from ._cleanup import cleanup 
from ._runthis import run_this
from .flatten import str_flatten

def bottom(self, silent = True, cores = 1):
    """
    Extract the bottom level from a tracker 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the bottom level
    """

    # extract the number of the bottom level
    # Use the first file for an ensemble
    # pull the cdo command together, then run it or store it
    if type(self.current) is list:
        ff = self.current[0]
        print("warning: first file in ensemble used to determine number of vertical levels")
    else:
        ff = self.current

    n_levels = int(os.popen( "cdo nlevel " + ff).read().split("\n")[0])

    cdo_command = "cdo -sellevidx," + str(n_levels)

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)

def surface(self, silent = True, cores = 1):
    """
    Extract the top/surface level from a tracker 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the surface level
    """

    cdo_command = "cdo -sellevidx,1 "
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    cleanup(keep = self.current)


def vertical_interp(self, vert_depths = None, silent = True, cores = 1):
    """
    Verticaly interpolate a tracker based on given depths

    Parameters
    -------------
    vert_depths : list
        list of depths to vertical interpolate to
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the surface level
    """
     
    # below used for checking whether vertical remapping occurs

    vertical_remap = True
       
    # first a quick fix for the case when there is only one vertical depth

    if vert_depths != None:
        if (type(vert_depths) == int) or (type(vert_depths) == float):
            vert_depths = {vert_depths}

  #  if vert_depths == None:
  #      vertical_remap = False
  #  
  #  if vert_depths != None:
  #      num_depths = len(self.depths())
  #      if num_depths < 2:
  #          print("There are none or one vertical depths in the file. Vertical interpolation not carried out.")
  #          vertical_remap = False
  #  if ((vert_depths != None) and vertical_remap):
  #      available_depths = self.depths() 
    
    # Check if min/max depths are outside valid ranges. This should possibly be a warning, not error
    if vertical_remap:
   #     if (min(vert_depths) < min(available_depths)):
   #          raise ValueError("error:minimum depth supplied is too low")
   #     if (max(vert_depths) > max(available_depths)):
   #          raise ValueError("error: maximum depth supplied is too low")

        vert_depths = str_flatten(vert_depths, ",")
        cdo_command = "cdo intlevel," + vert_depths
        
        run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

     # throw error if cdo fails at this point
    
    
    cleanup(keep = self.current)


def vertstat(self, stat = "mean", silent = True, cores = 1):
    """Method to calculate the vertical mean from a function""" 
    cdo_command = "cdo -vert" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

def vertical_mean(self, silent = True, cores = 1):
    """
    Calculate the depth-averaged mean 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the depth-averaged mean
    """

    return vertstat(self, stat = "mean", silent = True, cores = cores)

def vertical_min(self, silent = True, cores = 1):
    """
    Calculate the depth-averaged minimum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the depth-averaged minimum
    """

    return vertstat(self, stat = "min", silent = True, cores = cores)

def vertical_max(self, silent = True, cores = 1):
    """
    Calculate the depth-averaged maximum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the depth-averaged maximum
    """

    return vertstat(self, stat = "max", silent = True, cores = cores)
    
def vertical_range(self, silent = True, cores = 1):
    """
    Calculate the depth-averaged range 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracke
        Reduced tracker with the depth-averaged range
    """

    return vertstat(self, stat = "range", silent = True, cores = cores)
