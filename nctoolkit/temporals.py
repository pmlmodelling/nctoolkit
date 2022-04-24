from nctoolkit.runthis import run_this

def hourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -hour{stat}"

    run_this(cdo_command, self, output="ensemble")

def yhourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -yhour{stat}"

    run_this(cdo_command, self, output="ensemble")

def dhourstat(self, stat="mean"):
    """Method to calculate the hourly statistic from a function"""

    cdo_command = f"cdo -dhour{stat}"

    run_this(cdo_command, self, output="ensemble")

def ymonstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -ymon{stat}"

    run_this(cdo_command, self, output="ensemble")


def yearlystat(self, stat="mean"):
    """Function to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -year{stat}"

    run_this(cdo_command, self, output="ensemble")


def ydaystat(self, stat="mean"):
    """
    Method to calculate daily climatologies
    """
    # create the cdo command and run it
    cdo_command = "cdo -yday" + stat
    run_this(cdo_command, self, output="ensemble")


def seasclim(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""
    # create cdo call and run it
    cdo_command = f"cdo -yseas{stat}"

    run_this(cdo_command, self, output="ensemble")


def dailystat(self, stat="mean"):
    """Function to calculate the daily statistic for a function"""

    cdo_command = f"cdo -day{stat}"

    run_this(cdo_command, self, output="ensemble")


def monstat(self, stat="mean"):
    """Method to calculate the monthly statistic from a netCDF file"""
    cdo_command = f"cdo -mon{stat}"

    run_this(cdo_command, self, output="ensemble")


def seasstat(self, stat="mean"):
    """Method to calculate the seasonal statistic from a function"""

    cdo_command = f"cdo -seas{stat}"

    run_this(cdo_command, self, output="ensemble")
