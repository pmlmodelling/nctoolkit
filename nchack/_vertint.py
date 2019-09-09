from ._cleanup import cleanup
from ._runthis import run_this
from .flatten import str_flatten

def vertical_interp(self, vert_depths = None, silent = True, cores = 1):
    """Method to perform vertical interpolation on a netcdf file"""
     
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

    #return self
