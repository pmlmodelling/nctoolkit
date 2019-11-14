from ._runthis import run_this

def ymonstat(self, stat = "mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = "cdo -ymon" + stat

    run_this(cdo_command, self,  output = "ensemble")



def monthly_mean_climatology(self):
    """
    Calculate the monthly mean climatologies.  This applies to each file in an ensemble.

    """
    return ymonstat(self, stat = "mean")

def monthly_min_climatology(self):
    """
    Calculate the monthly minimum climatologies.  This applies to each file in an ensemble.

    """
    return ymonstat(self, stat = "min")

def monthly_max_climatology(self):
    """
    Calculate the monthly maximum climatologies.  This applies to each file in an ensemble.

    """
    return ymonstat(self,  stat = "max")

def monthly_range_climatology(self):
    """
    Calculate the monthly range climatologies.  This applies to each file in an ensemble.

    """
    return ymonstat(self, stat = "range")
