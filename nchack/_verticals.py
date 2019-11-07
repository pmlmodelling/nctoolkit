
import subprocess

from ._runthis import run_this
from .flatten import str_flatten

def bottom(self,  cores = 1):
    """
    Extract the bottom level from a dataset 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    # extract the number of the bottom level
    # Use the first file for an ensemble
    # pull the cdo command together, then run it or store it
    if type(self.current) is list:
        ff = self.current[0]
        print("warning: first file in ensemble used to determine number of vertical levels")
    else:
        ff = self.current

    cdo_result = subprocess.run("cdo nlevel " + ff, shell = True, capture_output = True)
    n_levels = int(str(cdo_result.stdout).replace("b'", "").strip().replace("'", "").split("\\n")[0])

    cdo_command = "cdo -sellevidx," + str(n_levels)

    run_this(cdo_command, self,  output = "ensemble", cores = cores)


def surface(self,  cores = 1):
    """
    Extract the top/surface level from a dataset 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    cdo_command = "cdo -sellevidx,1 "
    run_this(cdo_command, self,  output = "ensemble", cores = cores)


def vertical_interp(self, vert_depths = None,  cores = 1):
    """
    Verticaly interpolate a dataset based on given depths

    Parameters
    -------------
    vert_depths : list
        list of depths to vertical interpolate to
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

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
        
        run_this(cdo_command, self,  output = "ensemble", cores = cores)

     # throw error if cdo fails at this point
    
    


def vertstat(self, stat = "mean",  cores = 1):
    """Method to calculate the vertical mean from a function""" 
    cdo_command = "cdo -vert" + stat

    run_this(cdo_command, self,  output = "ensemble", cores = cores)

    # clean up the directory

def vertical_mean(self,  cores = 1):
    """
    Calculate the depth-averaged mean 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return vertstat(self, stat = "mean",  cores = cores)

def vertical_min(self,  cores = 1):
    """
    Calculate the depth-averaged minimum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return vertstat(self, stat = "min",  cores = cores)

def vertical_max(self,  cores = 1):
    """
    Calculate the depth-averaged maximum 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return vertstat(self, stat = "max",  cores = cores)
    
def vertical_range(self,  cores = 1):
    """
    Calculate the depth-averaged range 

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    """

    return vertstat(self, stat = "range",  cores = cores)
