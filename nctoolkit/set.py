def set(self, **kwargs):
    """
    A method for setting the units, names, and long names of the dataset.

    Operations are applied in the order supplied.

    Parameters
    -------------
    *kwargs
        Possible arguments: units, names, long_names

    """

    non_selected = True

    for key in kwargs:
        if key.lower() in ["unit", "units"]:
            self.set_units(kwargs[key])
            non_selected = False
        if "long" in key.lower() and "name" in key.lower():
            self.set_longnames(kwargs[key])
            non_selected = False

        if key.lower() == "names":
            self.rename(kwargs[key])
            non_selected = False

    if non_selected:
        raise ValueError("Please provide valid arg to set")
