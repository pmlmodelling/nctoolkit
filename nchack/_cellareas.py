import copy
from ._runthis import run_this
from ._runthis import run_cdo
from ._temp_file import temp_file
from ._cleanup import cleanup
from ._session import nc_safe


def cell_areas(self, cores = 1, join = True):
    """
    Calculate the cell areas in square meters

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 
    join: boolean
        Set to False if you only want the cell areas to be in the output. True joins the areas to the files.

    """

    lazy_eval = False

    if join and self.run == False:
        self.release()
        self.run = False 

    if join:
        target = temp_file(".nc")

        cdo_command = "cdo -gridarea " + self.current + " " + target

        run_cdo(cdo_command, target)

        self.history.append(cdo_command)
        
        new_target = temp_file(".nc")

        cdo_command = "cdo -L -merge " + self.current + " " + target + " " + new_target

        run_cdo(cdo_command, new_target)

        self.history.append(cdo_command)
        self.hold_history = copy.deepcopy(self.history)

        nc_safe.append(new_target)

        self.current = new_target

        cleanup()

    else:
        run_this(cdo_command, self,  output = "ensemble", cores = cores)


    self.set_units({"cell_area": "m2"})





