import subprocess


def nc_times(ff):
    """
    Function to return times available in a netCDF file
    """

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
    return cdo_result


def nc_format(ff):
    """
    Function to return the format of a netCDF file
    """

    cdo_result = subprocess.run(
        f"cdo showformat {ff}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    return cdo_result


def nc_levels(ff):
    """
    Function to get the depths available in a netCDF file
    """

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
    """
    Function to get the years available in a netCDF file
    """

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
    """
    Function to get the variables available in a netCDF file
    """

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


def nc_months(ff):
    """
    Function to get the months available in a netCDF file
    """

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
    all_months = list(set(cdo_result))
    all_months = [int(v) for v in all_months]
    all_months.sort()
    return all_months
