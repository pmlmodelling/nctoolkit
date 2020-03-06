from .runthis import run_this

def yearlystat(self, stat = "mean"):
    """Function to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -year{stat}"

    run_this(cdo_command, self,  output = "ensemble")




def annual_mean(self):
    """
    Calculate the yearly mean


    """
    return yearlystat(self, stat = "mean")

def annual_min(self):
    """
    Calculate the yearly minimum

    """
    return yearlystat(self, stat = "min")

def annual_max(self):
    """
    Calculate the yearly maximum

    """
    return yearlystat(self, stat = "max")

def annual_range(self):
    """
    Calculate the yearly range

    """
    return yearlystat(self, stat = "range")
