Creating variables
==================

**Please note: this method currently only works for the development
version of nctoolkit, and the feature will be available in the public
release on pypi and conda-forge in February 2021. This is a new feature,
that has been thorougly tested, but any feedback on error messages will
be appreciated.**

Variable creation in nctoolkit can be done using the ``assign`` method,
which works in a similar way to the method available in Pandas. As with
other tutorials on this site, we can use a global sea surface
temperature set available from NOAA which is described
`here <https://psl.noaa.gov/data/gridded/data.cobe2.html>`__.

.. code:: ipython3

    import nctoolkit as nc


The ``assign`` method works using lambda functions. Let’s say we have a
dataset with a variable 'var' and we simply want to add 10 to it and call
the new variable 'new'. We would do the following:

.. code:: ipython3

    data.assign(new = lambda x: x.var + 10)

If you are unfamilar with lambda functions, note that the x after lambda 
signifies that x represents the dataset in whatever comes after ':', which
is the actual equation to evaluate. The `x.var` term is `var` from the dataset.

By default assign keeps the original variables in the dataset.  However, we may 
only want the new variable or variables. In that case you can use the drop argument:

.. code:: ipython3

    data.assign(new = lambda x: x.var+ 10, drop = True)

This results in only one variable.

Note that the ``assign`` method uses kwargs for the lambda functions, so
drop can be positioned anywhere. So the following will do the same thing

.. code:: ipython3

    data.assign(new = lambda x: x.var+ 10, drop = True)
    data.assign(drop = True, new = lambda x: x.var+ 10)

The `assign` method will evaluate the lambda functions sent to it for 
each grid cell for each time step. So every part of the lambda function
must evaluate to a number. So the following will work:

.. code:: ipython3

    k = 273.15
    data.assign(drop = True, sst_k = lambda x: x.sst + k)

However, if you set ``k`` to a string or anything other than a number it
will throw an error. For example, this will throw an error:

.. code:: ipython3

    k = "273.15"
    data.assign(drop = True, sst_k = lambda x: x.sst + k)

Applying mathematical functions to dataset variables
----------------------------------------------------

As part of your lambda function you can use a number of standard
mathematical functions. These all have the same names as those in numpy:
``abs``, ``floor``, ``ceil``, ``sqrt``, ``exp``, ``log10``, ``sin``,
``cos``, ``tan``, ``arcsin``, ``arccos`` and ``arctan``.

For example if you wanted to calculate the ceiling of a variable you
could do the following:

.. code:: ipython3

    data.assign(new = lambda x: ceil(x.old))

An example of using logs would be the following:


.. code:: ipython3

    data.assign(new = lambda x: log10(x.old+1))


Using spatial statistics
------------------------

The ``assign`` method carries out its calculations in each time step,
and you can access spatial statistics for each time step when generating
new variables. A series of functions are available that have the same
names as nctoolkit methods for spatial statistics: ``spatial_mean``,
``spatial_max``, ``spatial_min``, ``spatial_sum``, ``vertical_mean``,
``vertical_max``, ``vertical_min``, ``vertical_sum``, ``zonal_mean``,
``zonal_max``, ``zonal_min`` and ``zonal_sum``.

An example of the usefulness of these functions would be if you were working
with global temperature data and you wanted to map regions that are warmer than average.
You could do this be by working out the difference between temperature in one location
and the global mean:

.. code:: ipython3

    data.assign(temp_comp = lambda x: x.temperature - spatial_mean(x.temperature), drop = True)

You can also do comparisons. In the above case, we instead might simply want to identify regions
that are hotter than the global average. In that case we can simply do this:

.. code:: ipython3

    data.assign(temp_comp = lambda x: x.temperature > spatial_mean(x.temperature), drop = True)

Let's say we wanted to map regions which are 3 degrees hotter than average. We could that as follows:

.. code:: ipython3

    data.assign(temp_comp = lambda x: x.temperature > spatial_mean(x.temperature + 3), drop = True)

or like this:

.. code:: ipython3

    data.assign(temp_comp = lambda x: x.temperature > (spatial_mean(x.temperature)+3), drop = True)

Logical operators work in the standard python way. So if we had a dataset with a variable called 'var'
and we wanted to find cells with values between 1 and 10, we could do this:

.. code:: ipython3

    data.assign(one2ten = lambda x: x.var > 1 & x.var < 10) 


You can process multiple variables at once using ``assign``. Variables
will be created in the order given, and variables created by the first
lambda function can be used by the next one, and so on. The simple
example below shows how this works. First we create a var1, which is
temperature plus 1. Then var2, which is var1 plus 1. Finally, we
calculate the difference between var1 and var2, and this should be 1
everywhere:

.. code:: ipython3

    data.assign(var1 = lambda x: x.var + 1, var2 = lambda x: x.var1 + 1, diff = lambda x: x.var2 - x.var1)

Functions that work with nctoolkit variables
--------------------------------------------

The following functions can be used on nctoolkit variables as part of
lambda functions.

+-----------------------+-----------------------+-----------------------+
| Function              | Description           | Example               |
+=======================+=======================+=======================+
| ``abs``               | Absolute value        | ``abs(x.sst)``        |
+-----------------------+-----------------------+-----------------------+
| ``floor``             | Floor of variable     | `                     |
|                       |                       | `floor(x.sst + 8.2)`` |
+-----------------------+-----------------------+-----------------------+
| ``ceiling``           | Ceiling of variable   | ``ceiling(x.sst -1)`` |
+-----------------------+-----------------------+-----------------------+
| ``sqrt``              | Square root of        | ``s                   |
|                       | variable              | qrt(x.sst + 273.15)`` |
+-----------------------+-----------------------+-----------------------+
| ``exp``               | Exponential of        | ``exp(x.sst)``        |
|                       | variable              |                       |
+-----------------------+-----------------------+-----------------------+
| ``log10``             | Base log10 of         | ``log10(x.sst + 1)``  |
|                       | variable              |                       |
+-----------------------+-----------------------+-----------------------+
| ``log``               | Natural log of        | ``log10(x.sst + 1)``  |
|                       | variable              |                       |
+-----------------------+-----------------------+-----------------------+
| ``sin``               | Trigonometric sine of | ``sin(x.var)``        |
|                       | variable              |                       |
+-----------------------+-----------------------+-----------------------+
| ``cos``               | Trigonometric cosine  | ``cos(x.var)``        |
|                       | of variable           |                       |
+-----------------------+-----------------------+-----------------------+
| ``tan``               | Trigonometric tangent | ``tan(x.var)``        |
|                       | of variable           |                       |
+-----------------------+-----------------------+-----------------------+
| ``spatial_mean``      | Spatial mean of       | ``                    |
|                       | variable at time-step | spatial_mean(x.var)`` |
+-----------------------+-----------------------+-----------------------+
| ``spatial_max``       | Spatial max of        | `                     |
|                       | variable at time-step | `spatial_max(x.var)`` |
+-----------------------+-----------------------+-----------------------+
| ``spatial_min``       | Spatial min of        | `                     |
|                       | variable at time-step | `spatial_min(x.var)`` |
+-----------------------+-----------------------+-----------------------+
| ``spatial_sum``       | Spatial sum of        | `                     |
|                       | variable at time-step | `spatial_sum(x.var)`` |
+-----------------------+-----------------------+-----------------------+
| ``zonal_mean``        | Zonal mean of         | ``zonal_mean(x.var)`` |
|                       | variable at time-step |                       |
+-----------------------+-----------------------+-----------------------+
| ``zonal_max``         | Zonal max of variable | ``zonal_max(x.var)``  |
|                       | at time-step          |                       |
+-----------------------+-----------------------+-----------------------+
| ``zonal_min``         | Zonal min of variable | ``zonal_min(x.var)``  |
|                       | at time-step          |                       |
+-----------------------+-----------------------+-----------------------+
| ``zonal_sum``         | Zonal sum of variable | ``zonal_sum(x.var)``  |
|                       | at time-step          |                       |
+-----------------------+-----------------------+-----------------------+
| ``isnan``             | Is variable a missing | ``isnan(x.var)``      |
|                       | value/NA?             |                       |
+-----------------------+-----------------------+-----------------------+
| ``cell_area``         | Area of grid-cell     | ``cell_area(x.var)``  |
|                       | (m2)                  |                       |
+-----------------------+-----------------------+-----------------------+
| ``isnan``             | Is variable a missing | ``isnan(x.var)``      |
|                       | value/NA?             |                       |
+-----------------------+-----------------------+-----------------------+
| ``level``             | Vertical level of     | ``level(x.var)``      |
|                       | variable. Example:    |                       |
|                       | depth in ocean data.  |                       |
+-----------------------+-----------------------+-----------------------+
| ``timestep``          | Time step of          | ``timestep(x.var)``   |
|                       | variable. Using       |                       |
|                       | Python indexing.      |                       |
+-----------------------+-----------------------+-----------------------+
| ``longitude``         | Longitude of the grid | ``longitude(x.var)``  |
|                       | cell                  |                       |
+-----------------------+-----------------------+-----------------------+
| ``latitude``          | Latitude of the grid  | ``latitude(x.var)``   |
|                       | cell                  |                       |
+-----------------------+-----------------------+-----------------------+
| ``year``              | Year of the variable  | ``year(x.var)``       |
+-----------------------+-----------------------+-----------------------+
| ``month``             | Month of the variable | ``month(x.var)``      |
+-----------------------+-----------------------+-----------------------+
| ``day``               | Day of the month of   | ``day(x.var)``        |
|                       | the variable          |                       |
+-----------------------+-----------------------+-----------------------+
| ``hour``              | Hour of the day of    | ``hour(x.var)``       |
|                       | the variable          |                       |
+-----------------------+-----------------------+-----------------------+

