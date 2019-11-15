import copy
from .runthis import run_this
from .runthis import run_cdo
from .temp_file import temp_file
from .cleanup import cleanup
from .session import nc_safe


def cell_areas(self,  join = True):
    """
    Calculate the cell areas in square meters

    Parameters
    -------------
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
        run_this(cdo_command, self,  output = "ensemble")


    self.set_units({"cell_area": "m2"})





