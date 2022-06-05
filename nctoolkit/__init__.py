from nctoolkit.api import (
    open_data,
    open_geotiff,
    from_xarray,
    merge,
    cor_time,
    cor_space,
    options,
    DataSet,
    open_thredds,
    open_url,
)

from nctoolkit.unify import unify

from nctoolkit.validator import validator
from nctoolkit.matchpoint import open_matchpoint


from nctoolkit.cleanup import cleanup, clean_all, deep_clean, temp_check
from nctoolkit.create_ensemble import create_ensemble
from nctoolkit.session import session_files
from nctoolkit.show import nc_variables, nc_years, nc_months, nc_times

from nctoolkit.utils import validate_version, cdo_version
from nctoolkit.session import session_info
from nctoolkit.mp_adders import match_points

session_info["cdo"] = cdo_version()

validate_version()
