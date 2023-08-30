def is_integer(x):
    try:
        y = int(str(x))
        return True
    except:
        return False


def fix_expr(expression):
    """
    Function to to convert operations to something cdo can handle
    """

    expression = expression.replace(" ", "")

    # equal constant case
    if expression.startswith("==-"):
        if (
            expression.replace("==-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("==", "eqc")
        expression = expression.replace("eqc", "eqc,")
        return expression
    # equal constant case
    if expression.startswith("=="):
        if (
            expression.replace("==", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("==", "eqc")
        expression = expression.replace("eqc", "eqc,")
        return expression

    # not equal constant case
    if expression.startswith("!=-"):
        if (
            expression.replace("!=-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("!=", "nec")
        expression = expression.replace("nec", "nec,")
        return expression
    # not equal constant case
    if expression.startswith("!="):
        if (
            expression.replace("!=", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("!=", "nec")
        expression = expression.replace("nec", "nec,")
        return expression

    # less than or equal to constant case
    if expression.startswith("<=-"):
        if (
            expression.replace("<=-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<=", "lec")
        expression = expression.replace("lec", "lec,")
        return expression

    # less than or equal to constant case
    if expression.startswith("<="):
        if (
            expression.replace("<=", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<=", "lec")
        expression = expression.replace("lec", "lec,")
        return expression

    # less than or equal to constant case
    if expression.startswith("<-"):
        if (
            expression.replace("<-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<", "ltc")
        expression = expression.replace("ltc", "ltc,")
        return expression
    # less than or equal to constant case
    if expression.startswith("<"):
        if (
            expression.replace("<", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<", "ltc")
        expression = expression.replace("ltc", "ltc,")
        return expression

    # greater than or equal to constant case
    if expression.startswith(">=-"):
        if (
            expression.replace(">=-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">=", "gec")
        expression = expression.replace("gec", "gec,")
        return expression

    if expression.startswith(">="):
        if (
            expression.replace(">=", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">=", "gec")
        expression = expression.replace("gec", "gec,")
        return expression

    # greater than or equal to constant case
    if expression.startswith(">-"):
        if (
            expression.replace(">-", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">", "gtc")
        expression = expression.replace("gtc", "gtc,")
        return expression

    if expression.startswith(">"):
        if (
            expression.replace(">", "").replace(".", "", 1).replace("e", "").isdigit()
            is False
        ):
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">", "gtc")
        expression = expression.replace("gtc", "gtc,")
        return expression

    raise ValueError(expression + " is not valid!")


def compare(self, expression=None):
    """
    Compare all variables to a constant

    Parameters
    -------------
    expression: str
        This a regular comparison such as "<0", ">0", "==0"

    Examples
    ------------

    If you wanted to identify grid cells with positive values you would do the following:

    >>> ds.compare(">0")

    This could also be done using standard python syntax:

    >>> ds > 0

    This will be calculcated for each time step.

    If you wanted to identify grid cells with negative values, you would do this

    >>> ds.compare("<0")

    This could also be done using standard python syntax:

    >>> ds < 0


    """

    if expression is None:
        raise ValueError("No expression supplied")

    if not isinstance(expression, str):
        raise TypeError("Expression supplied is not str")

    expression = fix_expr(expression)
    cdo_command = f"-{expression}"
    self.cdo_command(cdo_command, ensemble=False)


def __eq__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f"=={x_new}")
        except:
            self.eq(x)
    else:
        self.eq(x)


def __gt__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f">{x_new}")
        except:
            self.gt(x)
    else:
        self.gt(x)


def __lt__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f"<{x_new}")
        except:
            self.lt(x)
    else:
        self.lt(x)


def __le__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f"<={x_new}")
        except:
            self.le(x)
    else:
        self.le(x)


def __ge__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f">={x_new}")
        except:
            self.ge(x)
    else:
        self.ge(x)


def __ne__(self, x):
    if not isinstance(x, str):
        try:
            test = float(x)
            x_new = x
            if not is_integer(x):
                x_new = str(float(x)).replace("+", "")
            self.compare(f"!={x_new}")
        except:
            self.ne(x)
    else:
        self.ne(x)
