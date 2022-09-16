def sum_all(self, drop=True):
    """
    Calculate the sum of all variables for each time step

    Parameters
    -------------
    drop : boolean
        Do you want to keep variables?
    """

    self.run()

    contents = self.contents

    easy = True
    if len(self) > 1:
        for x in self.contents.reset_index().loc[:,["file", "variable"]].groupby("variable").size().values:
            if x != len(self):
                easy = False

    if (len(self) > 1 and easy is False) and (self._merged is False):
        raise TypeError("This currently only works for datasets with files with the same variables")

    if drop is True:
        self.cdo_command("expr,total=" + "+".join(self.variables))

    else:
        if "total" not in self.variables:
            self.cdo_command("aexpr,total=" + "+".join(self.variables))
        else:
            i = 0
            while True:
                if f"total{i}" not in self.variables:
                    break
                i += 1
            self.cdo_command("aexpr,total" + str(i) + "=" + "+".join(self.variables))
