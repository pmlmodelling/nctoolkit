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
        Set to False if you only want the cell areas to be in the output. join=True adds the areas as a variable to the dataset.

    """

    # release if you need to join the cell areas to the original file
    if join:
        self.release()

        if type(self.current) is list:
            raise TypeError("This only works with single file datasets at present!")

    # first run the join case
    if join:
        target = temp_file(".nc")

        cdo_command = "cdo -L -merge " + self.current + " -gridarea " + self.current + " " + target
        target = run_cdo(cdo_command, target)

        self.history.append(cdo_command)
        self._hold_history = copy.deepcopy(self.history)

        nc_safe.append(target)

        if self.current in nc_safe:
            nc_safe.remove(self.current)
        self.current = target

        cleanup()

    else:

        cdo_command = "-gridarea"
        run_this(cdo_command, self,  output = "ensemble")


    # add units
    self.set_units({"cell_area": "m^2"})





