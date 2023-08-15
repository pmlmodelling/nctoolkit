import re
import subprocess


def name_check(x):
    """
    Function to check whether a string is a valid variable name
    """
    if len(x) == 0:
        return False

    if " " in x:
        return False

    text = re.compile(".*[+,/,-,*]")
    if len(text.findall(x)) > 0:
        return False

    if len(x) == 1:
        text = re.compile("[a-zA-Z]")
        if text.match(x):
            return True
        else:
            return False
    text = re.compile("([a-zA-Z0-9_]|{MUTF8})([^\x00-\x1F/\x7F-\xFF]|{MUTF8})")
    # regex taken from https://www.unidata.ucar.edu/support/help/MailArchives/netcdf/msg10684.html

    if text.match(x):
        return True
    else:
        return False


def is_curvilinear(ff):
    """
    Function to work out if a file contains a curvilinear grid
    """
    cdo_result = subprocess.run(
        f"cdo sinfo {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return (
        len(
            [
                x
                for x in cdo_result.stdout.decode("utf-8").split("\n")
                if "curvilinear" in x
            ]
        )
        > 0
    )


def version_below(x, y):
    x = x.split(".")
    x = int(x[0]) * 1000 + int(x[1]) * 100 + int(x[2])

    y = y.split(".")
    y = int(y[0]) * 1000 + int(y[1]) * 100 + int(y[2])

    return x < y



def validate_version(version):
    """
    Function to tell the user whether a valid version of CDO is installed
    """
    bad = True
    try:
        if version_below(version, "2.0.5") is False:
                print(
                    f"nctoolkit is using Climate Data Operators version {version}"
                )
                bad = False
    except:
        bad = True

    if bad:
        try:
            error = (
                f"This version of nctoolkit requires CDO>=2.0.5. Please install a recent version of CDO. You have version {version}."
            )
        except:
            raise ValueError(
                f"This version of nctoolkit requires CDO>=2.0.5. Please install a recent version of CDO."
            )
        raise ValueError(error)



def cdo_version():
    """
    Function to identify the CDO version
    """
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    version = [
        x for x in str(cdo_check.stderr).split("\n") if "version" in x and "cdo" in x
    ]
    if len(version) == 0:
        version = [
            x
            for x in str(cdo_check.stdout).split("\n")
            if "version" in x and "cdo" in x
        ]
        if len(version) == 0:
            return None
    version = version[0]

    candidates = [
        x for x in version.split(" ") if x.startswith("1") or x.startswith("2")
    ]
    version = candidates[0]
    validate_version(version)
    return version 
