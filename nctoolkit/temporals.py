def hourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -hour{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def yhourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -yhour{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def dhourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -dhour{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def ymonstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -ymon{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def yearlystat(self, stat="mean"):
    """Function to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -year{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def ydaystat(self, stat="mean"):
    """
    Method to calculate daily climatologies
    """
    # create the cdo command and run it
    cdo_command = "cdo -yday" + stat

    self.cdo_command(cdo_command, ensemble=False)


def seasclim(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""
    # create cdo call and run it
    cdo_command = f"cdo -yseas{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def dailystat(self, stat="mean"):
    """Function to calculate the daily statistic for a function"""

    cdo_command = f"cdo -day{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def monstat(self, stat="mean"):
    """Method to calculate the monthly statistic from a netCDF file"""
    cdo_command = f"cdo -mon{stat}"

    self.cdo_command(cdo_command, ensemble=False)


def seasstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -seas{stat}"

    self.cdo_command(cdo_command, ensemble=False)
