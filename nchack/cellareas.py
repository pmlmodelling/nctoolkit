import copy
from .runthis import run_this
from .runthis import run_cdo
from .temp_file import temp_file
from .cleanup import cleanup
from .session import nc_safe
from .show import nc_variables


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


    # first run the join case
    if join:

        if type(self.current) is str:
            self.current = [self.current]


        new_files = []
        new_commands = []

        for ff in self.current:

            if "cell_area" in nc_variables(ff):
                raise ValueError("cell_area is already a variable")


            target = temp_file(".nc")


            cdo_command = "cdo -L -merge " + ff + " -gridarea " + ff + " " + target
            target = run_cdo(cdo_command, target)
            new_files.append(target)

            new_commands.append(cdo_command)

            nc_safe.append(target)

        for ff in self.current:
            if ff in nc_safe:
                nc_safe.remove(ff)


        for x in new_commands:
            self.history.append(x)

        self.current = new_files

        self._hold_history = copy.deepcopy(self.history)

        cleanup()

    else:

        cdo_command = "-gridarea"
        run_this(cdo_command, self,  output = "ensemble")


    # add units

    if join:
        self.set_units({"cell_area": "m^2"})
    else:
        self.set_units({"cell_area": "m^2"})





