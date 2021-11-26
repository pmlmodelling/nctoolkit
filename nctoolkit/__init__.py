from nctoolkit.api import (
    open_data,
    from_xarray,
    merge,
    cor_time,
    cor_space,
    options,
    DataSet,
    open_thredds,
    open_url,
)
from nctoolkit.cleanup import cleanup, clean_all, deep_clean, temp_check
from nctoolkit.create_ensemble import create_ensemble
from nctoolkit.session import session_files
from nctoolkit.show import nc_variables, nc_years, nc_months, nc_times

import re
import subprocess

# check version of cdo installed

from nctoolkit.utils import validate_version, cdo_version
from nctoolkit.session import session_info

session_info["cdo"] = cdo_version()

validate_version()
