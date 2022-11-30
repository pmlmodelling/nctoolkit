from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this


def mask_box(self, lon=[-180, 180], lat=[-90, 90]):
    """
    Mask a lon/lat box

    Parameters
    -------------
    lon : list
        Longitude range to mask. Must be of the form: [lon_min, lon_max]
    lat : list
        Latitude range to mask. Must be of the form: [lat_min, lat_max]
    """

    if not isinstance(lon, list) or  not isinstance(lat, list):
        raise TypeError("Check that lon/lat ranges are tuples")

    if len(lon) != 2:
        raise ValueError("lon is a list of more than 2 variables")

    if len(lat) != 2:
        raise ValueError("lat is a list of more than 2 variables")

    if not isinstance(lon[0], (int, float)):
        raise TypeError("Check lon")

    if not isinstance(lon[1], (int, float)):
        raise TypeError("Check lon")

    if not isinstance(lat[0], (int, float)):
        raise TypeError("Check lat")

    if not isinstance(lat[1], (int, float)):
        raise TypeError("Check lat")

    # now, clip to the lonlat box we need

    if lat[1] < lat[0]:
        raise ValueError("Check lat order")
    if lon[1] < lon[0]:
        raise ValueError("Check lon order")

    # now, clip to the lonlat box we need

    if (lon[0] >= -180) and (lon[1] <= 180) and (lat[0] >= -90) and (lat[1] <= 90):

        lat_box = str_flatten(lon + lat)
        cdo_command = f"cdo -masklonlatbox,{lat_box}"
        run_this(cdo_command, self, output="ensemble")
    else:
        raise ValueError("The lonlat box supplied is not valid!")
