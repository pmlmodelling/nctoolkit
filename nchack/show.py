import subprocess
import pandas as pd
import warnings


def times(self):

    all_times = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo showtimestamp {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_times += cdo_result
    all_times = list(set(all_times))
    all_times.sort()
    return all_times


def levels(self):
    """
    Method to get the depths available in a netcdf file
    """
    if type(self.current) is list:
        warnings.warn(message="Levels available in first file shown!")
        ff = self.current[0]
    else:
        ff = self.current

    cdo_result = subprocess.run(
        f"cdo showlevel {ff}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result = [float(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result


def nc_years(ff):
    all_years = []
    cdo_result = subprocess.run(
        f"cdo showyear {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    all_years += cdo_result
    all_years = list(set(all_years))
    all_years = [int(v) for v in all_years]
    all_years.sort()
    return all_years


def nc_variables(ff):
    cdo_result = subprocess.run(
        f"cdo showname {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    return cdo_result


def years(self):

    all_years = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo showyear {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_years += cdo_result
    all_years = list(set(all_years))
    all_years = [int(v) for v in all_years]
    all_years.sort()
    return all_years


def months(self):

    all_months = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo showmon {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cdo_result = str(cdo_result.stdout).replace("\\n", "")
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.replace("'", "").strip()
        cdo_result = cdo_result.split()
        all_months += cdo_result
    all_months = list(set(all_months))
    all_months = [int(v) for v in all_months]
    all_months.sort()
    return all_months


