from ._cleanup import cleanup
from ._runthis import run_this
from ._runthis import run_cdo
from ._temp_file import temp_file
from ._filetracker import nc_created


def cell_areas(self, silent = True, cores = 1, join = True):
    """
    Calculate the cell areas in square meters

    Parameters
    -------------
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with cell areas 

    """

    if join and self.run == False:
        self.release()

    if join:
        target = temp_file(".nc")
        nc_created.append(target)
        cdo_command = "cdo -gridarea " + self.current + " " + target
        self.history.append(cdo_command)
        run_cdo(cdo_command, target)
        
        new_target = temp_file(".nc")
        nc_created.append(new_target)
        cdo_command = "cdo -L -merge " + self.current + " " + target + " " + new_target
        self.history.append(cdo_command)
        run_cdo(cdo_command, new_target)
        self.current = new_target
    else:
        run_this(cdo_command, self, silent, output = "ensemble", cores = cores)



    cleanup(keep = self.current)
