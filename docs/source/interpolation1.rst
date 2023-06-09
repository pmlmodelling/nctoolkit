Interpolation
============

nctoolkit features built in methods for horizontal and vertical interpolation.

Horizontal interpolation
-------------------------

We will illustrate how to carry out horizontal interpolation using a global dataset of global SST from NOAA. Find out more information about the datset `here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.


The data is available using a thredds server. So we will work with the first time step, which looks like this:


.. code:: ipython3


   import nctoolkit as nc
   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(time = 0)
   ds.plot()

.. raw:: html
   :file: visualization_plot1.html


Interpolating to a set of coordinates

--------------------------------------


If you want to regrid a dataset to a specified set of coordinates you
can ``regrid`` and a pandas dataframe. The first column of the dataframe
should be the longitudes and the second should be latitudes. The example
below regrids a sea-surface temperature dataset to a single location
with longitude -30 and latitude 50.


.. code:: ipython3

   import pandas as pd
   ds = nc.open_thredds("https://psl.noaa.gov/thredds/dodsC/Datasets/COBE2/sst.mon.mean.nc")
   ds.subset(timestep = 0) 
   coords = pd.DataFrame({"lon":[-30], "lat":[50]})
   ds.regrid(coords)
   ds.to_dataframe()


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>lon</th>
          <th>lat</th>
          <th>sst</th>
        </tr>
        <tr>
          <th>time</th>
          <th>ncells</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1850-01-01</th>
          <th>0</th>
          <td>-30.0</td>
          <td>50.0</td>
          <td>10.935501</td>
        </tr>
      </tbody>
    </table>
    </div>



Plotting internals
---------------------
Plotting is carried out using the ncplot package. ncplot will look at the dataset and identify a suitable plotting method. This is carried out internally using hvplot. If you come across any errors, 
please raise an issue `here <https://github.com/pmlmodelling/ncplot>`__.

This is a package that aims to deliver plotting for rapid exploratory analysis, and therefore it does not offer a large number of customizations. However, because it is built on hvplot, you can use most of the customization options available in hvplot, which are detailed `here <https://hvplot.holoviz.org/user_guide/Customization.html>`__. Arguments such as `title`, `logz` and `clim` can be passed to `plot` and will be automatically passed to the hvplot method used
.





