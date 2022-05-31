import subprocess
from dateutil.parser import parse


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
    cdo_result = [
        x
        for x in " ".join(
            [
                x
                for x in cdo_result.stdout.decode("utf-8").split("\n")
                if "cdo" not in x and len(x) > 0
            ]
        )
        .replace("  ", " ")
        .split(" ")
        if len(x) > 0
    ]

    try:
        cdo_result = [parse(x) for x in cdo_result]
        return cdo_result
    except:
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
    return [
        x
        for x in cdo_result.stdout.decode("utf-8").split("\n")
        if "cdo" not in x and len(x) > 0
    ]


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
    return list(
        set(
            [
                float(x)
                for x in " ".join(
                    [
                        x
                        for x in cdo_result.stdout.decode("utf-8").split("\n")
                        if "cdo" not in x
                    ]
                ).split(" ")
                if len(x) > 0
            ]
        )
    )


def nc_years(ff):
    """
    Function to get the years available in a netCDF file
    """

    cdo_result = subprocess.run(
        f"cdo showyear {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return list(
        set(
            [
                int(x)
                for x in " ".join(
                    [
                        x
                        for x in cdo_result.stdout.decode("utf-8").split("\n")
                        if "cdo" not in x
                    ]
                ).split(" ")
                if len(x) > 0
            ]
        )
    )


def nc_variables(ff):
    """
    Function to get the variables available in a netCDF file
    """

    cdo_result = subprocess.run(
        f"cdo showname {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    new = " ".join([
    x
    for x in [
        x
        for x in cdo_result.stdout.decode("utf-8").split("\n")
        if "cdo" not in x and len(x) > 0
    ]
        if len(x) > 0
    ])
    return [x for x in new.split(" ") if len(x) > 0]
    #return [
    #    x
    #    for x in [
    #        x
    #        for x in cdo_result.stdout.decode("utf-8").split("\n")
    #        if "cdo" not in x and len(x) > 0
    #    ][0].split(" ")
    #    if len(x) > 0
    #]


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

    return list(
        set(
            [
                int(x)
                for x in " ".join(
                    [
                        x
                        for x in cdo_result.stdout.decode("utf-8").split("\n")
                        if "cdo" not in x
                    ]
                ).split(" ")
                if len(x) > 0
            ]
        )
    )
