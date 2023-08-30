def sum_all(self, drop=True, new_name=None):
    """
    sum_all: Calculate the sum of all variables for each time step

    Parameters
    -------------
    drop : boolean
        Do you want to keep variables?
    new_name : string
        If you want to name the output of sum_all to a specific name

    Examples
    -------------
    >>> ds.sum_all()
    Setting the name of the output to combined
    >>> ds.sum_all(new_name = "combined")

    """
    if new_name is not None:
        if not isinstance(new_name, str):
            raise TypeError("new_name must be a string")

    self.run()

    contents = self.contents

    easy = True
    if len(self) > 1:
        for x in (
            self.contents.reset_index()
            .loc[:, ["file", "variable"]]
            .groupby("variable")
            .size()
            .values
        ):
            if x != len(self):
                easy = False

    if (len(self) > 1 and easy is False) and (self._merged is False):
        raise TypeError(
            "This currently only works for datasets with files with the same variables"
        )

    if drop is True:
        if new_name is None:
            self.cdo_command("-expr,total=" + "+".join(self.variables))
        else:
            self.cdo_command("-expr," + new_name + "=" + "+".join(self.variables))
    else:
        if new_name is not None:
            self.cdo_command("-expr," + new_name + "=" + "+".join(self.variables))
            return None
        if "total" not in self.variables:
            self.cdo_command("-aexpr,total=" + "+".join(self.variables))
        else:
            i = 0
            while True:
                if f"total{i}" not in self.variables:
                    break
                i += 1
            self.cdo_command("-aexpr,total" + str(i) + "=" + "+".join(self.variables))
