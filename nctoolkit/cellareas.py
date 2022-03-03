import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.session import remove_safe, session_info
from nctoolkit.runthis import run_this, tidy_command, run_cdo
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file


def cell_area(self, join=True):
    """
    Calculate the area of grid cells.
    Area of grid cells is given in square meters.

    Parameters
    -------------
    join: boolean
        Set to False if you only want the cell areas to be in the output.
        join=True adds the areas as a variable to the dataset. Defaults to True.

    Examples
    ------------
    If you wanted to add the cell_areas as a new variable in a dataset, you would do the following:

    >>> ds.cell_area()

    If you wanted to replace a dataset with the cell areas of that dataset, you would do the following:

    >>> ds.cell_area(join = False)

    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    if isinstance(join, bool) is False:
        raise TypeError("join is not boolean")

    # release if you need to join the cell areas to the original file
    if join:
        self.run()

    # first run the join case
    if join:

        new_files = []
        new_commands = []

        for ff in self:

            if "cell_area" in nc_variables(ff):
                raise ValueError("cell_area is already a variable")

            target = temp_file(".nc")

            cdo_command = f"cdo -merge {ff} -gridarea {ff} {target}"
            cdo_command = tidy_command(cdo_command)
            target = run_cdo(cdo_command, target, precision=self._precision)

            new_files.append(target)

            new_commands.append(cdo_command)

        for x in new_commands:
            self.history.append(x)

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)

        self._hold_history = copy.deepcopy(self.history)

        cleanup()

    else:

        cdo_command = "cdo -gridarea"
        run_this(cdo_command, self, output="ensemble")

    # add units

    self.set_units({"cell_area": "m^2"})

    if join:
        self.run()
        self.disk_clean()
