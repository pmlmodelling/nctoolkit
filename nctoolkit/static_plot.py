from nctoolkit.session import session_info
try:
    import signal
    from contextlib import contextmanager
    from nctoolkit.session import session_info
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib as mpl
    
    from mpl_toolkits import axes_grid1
    
    from netCDF4 import Dataset
    import numpy as np
    
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import nctoolkit as nc
    
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    
    import sys
    
    ## this is to fix some bug in themodules that should be solved with the right version of modules loaded
    from matplotlib.axes import Axes
    from cartopy.mpl.geoaxes import GeoAxes
except: 
    session_info["static_plot"] = False

from textwrap import wrap



class TimeoutException(Exception):
    pass

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out. Try plotting fewer variables!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

from math import radians, sin, cos, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))

def static_plot(ds, extent = None, title = None, legend = None, size = "auto", land = "grey", colours = "auto", norm = None, limits = None, projection = "auto", mid_point = None, coast = "auto", scale = "medium", globe = False, **kwargs):
    """
    Static plotting. This requires datasets to have regular latlon grids.
    Plots a static map, and requires only one variable, time step and vertical level

    Parameters
    -------------
    extent: list 
        List with [lon_min, lon_max, lat_min, lat_max] to limit the map extent 
    title: str 
        Character string with plot title 
    legend: str 
        Character string with legend title 
    size: list 
        List with [xsize, ysize] for plotting size 
    land: str 
        Character string with colour required for land. Set to None if you do not want land to show.
    norm: str or matplotlib.colors norm
         Norm to use for colour bar 
    mid_point: float 
        Mid-point to use for colour bar 
    projection: cartopy projection 
        Cartopy projection to use.  
    coast: str 
        Set to "coarse", "low", "intermediate", "high" or "full" if you want to use GSHHS coastlines 
    scale: str 
        "low", "medium" or "high" 

    -------------
    """

    if "static_plot" in session_info.keys():
        raise ValueError("Unable to import cartopy properly")

    if coast not in ["auto", "coarse", "low", "intermediate", "high", "full"]:
        the_options = ",".join(["auto", "coarse", "low", "intermediate", "high", "full"])
        raise ValueError(f"coast must be one of {the_options}")


    options = ["extent",
            "title",
            "legend",
            "size",
            "land",
            "colours",
            "norm",
            "limits",
            "projection"]

    for kk in kwargs:
        fixed = False
        if kk.lower().startswith("col") and kk.lower().endswith("rs"):
            if colours == "viridis":
                colours = kwargs[kk]
                fixed = True

        if kk.lower().startswith("trans"):
            if norm == None:
                norm = kwargs[kk]
                fixed = True

        if kk.lower().startswith("mid") and kk.lower().endswith("nt"):
            if mid_point is None:
                mid_point = kwargs[kk]
                fixed = True

        if kk.lower().startswith("proj"):
            if projection == "auto":
                projection = kwargs[kk]
                fixed = True

        if kk.lower().startswith("norm"):
            if norm == None:
                norm = kwargs[kk]
                fixed = True

        if not fixed:
            possible = []

            for x in options:
                if similar(x.lower(), kk.lower()) > 0.6:
                    possible.append(x)

            if len(possible) > 0:
                part2 = ",".join(possible)
                raise ValueError(f"{kk} is not a valid argument. Did you mean one of these? {part2}")
            else:
                raise ValueError(f"{kk} is not a valid argument")

    ds.run()

    if len(ds.variables) > 1:
        raise ValueError("Only one variable wanted")
    if len(ds.times) > 1:
        raise ValueError("Only one timestep wanted")

    ds_xr = ds.to_xarray(decode_times = False)
    failed = False
    try:
        lon_name = [x for x in ds_xr.dims if "lon" in x][0]
        lat_name = [x for x in ds_xr.dims if "lat" in x][0]
    except:
        failed = True
    if failed:
        if "nav_lon" in ds_xr.coords and "nav_lat" in ds_xr.coords:
            try:
                ds.fix_nemo_ersem_grid()
                ds_xr = ds.to_xarray(decode_times = False)
                lon_name = [x for x in ds_xr.dims if "lon" in x][0]
                lat_name = [x for x in ds_xr.dims if "lat" in x][0]
            except:
                raise ValueError("Unable to parse coordinates")

    GeoAxes._pcolormesh_patched = Axes.pcolormesh

        # set data projection
        # here a Lambert conformal is used, more projections can be found here https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html

    input_file=Dataset(ds[0])

    #read the coordinates
    lat=input_file.variables[lat_name][:]
    lon=input_file.variables[lon_name][:]

    # set globe to True if lon lat spread is big enough

    if np.max(lon) - np.min(lon) > 358:
        if np.max(lat) - np.min(lat) > 176:
            globe = True

    #proj=ccrs.LambertConformal(central_longitude=np.mean(lon), central_latitude=np.mean(lat), false_easting=0.0, false_northing=0.0,  cutoff=38)

    # check coord type
    lambert = False

    if projection == "auto":
        if lat.min() < 0 and lat.max() > 0:
            proj=ccrs.PlateCarree()
        else:
            if (lon.max() - lon.min()) < 160:
                proj=ccrs.LambertConformal(central_longitude=np.mean(lon), central_latitude=np.mean(lat))
            else:
                proj=ccrs.PlateCarree()
    else:
        proj = projection
    data_crs=ccrs.PlateCarree()

    if globe:
        proj=ccrs.Robinson()

    if projection == None:
        proj=ccrs.PlateCarree()
    if size == "auto":
        size = [10, 10]
        if proj == ccrs.PlateCarree() or globe:
            size[1] = size[0] * float((np.max(lat)  - np.min(lat)))/float(( np.max(lon) - np.min(lon)    )) / 1.1
        else:
            size[1] = size[0] * haversine(min(lon), min(lat), min(lon), max(lat))/ haversine(min(lon), 0.4* (min(lat) + max(lat)), max(lon), 0.4 * (min(lat) + max(lat)))/ 1.1 
        # rescale to vertical height of 5
        max_size = max(size)
        size = [5 * size[0]/size[1], 5]

    #check how many dimensions the coordinate variables have. if they have 1 dimension only, then the grid need to be created
    if (len(lat.shape)==1) and (len(lon.shape)==1):
        lon,lat=np.meshgrid(lon,lat)
    elif (len(lat.shape)==1) or (len(lon.shape)==1):  # if the variable have different dimensions print an error
        sys.exit ('something is wrong in the input file. the coordiantes variables have different dimensions')
    else:
        pass

    # read the values. the array is squeezed to remove the temporal dimension that has length 1
    values=input_file.variables[ds.variables[0]][:].squeeze()

    # mask where the values is 0 == land points
    values=np.ma.masked_where(values==0,values)

    if mid_point is None and limits is None:
        min_value = np.min(values)
        max_value = np.max(values)
        if min_value < 0 and max_value > 0:
            mid_point = 0 
            colours = "coolwarm"

    if colours == "auto":
        colours = "viridis"

    # generate the figure and the axes where to plot the map. When the axes are generated (either with add_subplot or add_axes, or any other way), the projection to be used need to be specified
    # the axes generated show the entire globe up to the cutoff latitude
    if size is not None:
        fig=plt.figure(figsize=size)
    else:
        fig=plt.figure(figsize=(10,10))
    #plt.ioff()
    ax=fig.add_subplot(projection=proj)
    if globe:
        ax.set_global()

    # set the extension of the actual domain (i.e. the lat lon limits)
    # notice how the range is larger than the actual domain. this is due because with the chosen projection a larger canvas is needed to encompass the whole domain
    if extent is not None:
        ax.set_extent(extent)

    # plot the map. the critical bit is the "transform" option, where the projection of the data is specified. In this case spherical coordinates
    # the shading option is to let pcolormesh understand that the coordinates passed are the cell centre, see https://matplotlib.org/stable/gallery/images_contours_and_fields/pcolormesh_grids.html

    if limits is None:
        vmin = None 
        vmax = None 
    else:
        vmin = limits[0]
        vmax = limits[1]

    if mid_point is not None:
        val_min = values.min()
        val_max = values.max()
        if mid_point < val_min:
            raise ValueError("mid_point is outside value range")
        if mid_point > val_max:
            raise ValueError("mid_point is outside value range")
        adjustment = max(val_max - mid_point, mid_point - val_min)
        vmin = mid_point - adjustment
        vmax = mid_point + adjustment



    if norm == "log":
        norm = matplotlib.colors.LogNorm(vmin =vmin, vmax = vmax)
    if norm is not None:
        vmin = None
        vmax = None
    im=ax.pcolormesh(lon,lat,values,cmap= colours,transform=data_crs,shading='nearest', norm=norm, vmin = vmin, vmax = vmax)

    # add coastline and land colour. More options, including about resolution of coastline, colour and so on can be found here
    # https://scitools.org.uk/cartopy/docs/v0.14/matplotlib/feature_interface.html
    #
    # add grid lineshttp://localhost:8890/notebooks/Untitled4.ipynb?kernel_name=python3#
    # first define the gridliner object
    # crs define the units of the values (here spehric coorindates)
    # the other options are for grpahics, more details can be found here
    # https://scitools.org.uk/cartopy/docs/v0.13/matplotlib/gridliner.html
    # note that if x_inline and y_inline are not set to False, the labels of the axis could be written inside the map

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color='k', alpha=0.5, linestyle='--',x_inline=False, y_inline=False,)

    #gl.xlocator = mticker.FixedLocator([-20,-10,0,10])
    #gl.ylocator = mticker.FixedLocator([40,50,60])
    # here you can select on which side to write the labels for the grid
    gl.top_labels = True
    gl.bottom_labels= False
    gl.right_labels = False
    gl.left_labels = True

    # add title
    if title is not None:
        ax.set_title(title)

    # add colorbar

    fraction = 0.046* size[1]/size[0]
    

    cb=plt.colorbar(im, fraction = fraction, pad = 0.04) 
    cbax=cb.ax
    if land is not None:
        #ax.add_feature(cfeature.LAND, facecolor = land, zorder=10)
        if scale == "low":
            scale = "110m"
        if scale == "medium":
            scale = "50m"
        if scale == "high":
            scale = "10m"

        ax.add_feature(cfeature.NaturalEarthFeature(category = "physical", scale = scale,name = "land", facecolor = land, zorder=10))
    if coast is not None:
        if coast == "auto":
            ax.add_feature(cfeature.COASTLINE)
        else:
            ax.add_feature(cfeature.GSHHSFeature(scale = coast))


    if legend is not None:
        cbax.set_ylabel(legend)
    else:
        ds_contents = ds.contents
        try:
            label = ds_contents.long_name.values[0] + " (" +  ds_contents.unit.values[0] + ")"
        except:
            print("Unable to parse legend from dataset contents. Check long names and units")
            label = ""

        label = "\n".join(wrap(label, 50))

        cbax.set_ylabel(label)

