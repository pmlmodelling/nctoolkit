Manipulating variables
==================

Creating new variables
----------------------------------------------------


Variable creation in nctoolkit can be done using the ``assign`` method,
which works in a similar way to the method available in pandas. 

The ``assign`` method works using lambda functions. Let’s say we have a
dataset with a variable 'var' and we simply want to add 10 to it and call
the new variable 'new'. We would do the following:

.. code:: ipython3

    ds.assign(new = lambda x: x.var + 10)

If you are unfamilar with lambda functions, note that the x after lambda 
signifies that x represents the dataset in whatever comes after ':', which
is the actual equation to evaluate. The `x.var` term is `var` from the dataset.

By default assign keeps the original variables in the dataset.  However, we may 
only want the new variable or variables. In that case you can use the drop argument:

.. code:: ipython3

    ds.assign(new = lambda x: x.var+ 10, drop = True)

This results in only one variable.

Note that the ``assign`` method uses kwargs for the lambda functions, so
drop can be positioned anywhere. So the following will do the same thing

.. code:: ipython3

    ds.assign(new = lambda x: x.var+ 10, drop = True)
    ds.assign(drop = True, new = lambda x: x.var+ 10)


At present, ``assign`` requires that it is written on a single line. So avoid doing something
like the following:

.. code:: ipython3

    ds.assign(new = lambda x: x.var+ 10, drop = True)

The `assign` method will evaluate the lambda functions sent to it for 
each dataset grid cell for each time step. So every part of the lambda function
must evaluate to a number. So the following will work:

.. code:: ipython3

    k = 273.15
    ds.assign(drop = True, sst_k = lambda x: x.sst + k)

However, if you set ``k`` to a string or anything other than a number it
will throw an error. For example, this will throw an error:

.. code:: ipython3

    k = "273.15"
    ds.assign(drop = True, sst_k = lambda x: x.sst + k)

Applying mathematical functions to dataset variables
----------------------------------------------------

As part of your lambda function you can use a number of standard
mathematical functions. These all have the same names as those in numpy:
``abs``, ``floor``, ``ceil``, ``sqrt``, ``exp``, ``log10``, ``sin``,
``cos``, ``tan``, ``arcsin``, ``arccos`` and ``arctan``.

For example if you wanted to calculate the ceiling of a variable you
could do the following:

.. code:: ipython3

    ds.assign(new = lambda x: ceil(x.old))

An example of using logs would be the following:


.. code:: ipython3

    ds.assign(new = lambda x: log10(x.old+1))


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
You could do this by working out the difference between temperature in one location
and the global mean:

.. code:: ipython3

    ds.assign(temp_comp = lambda x: x.temperature - spatial_mean(x.temperature), drop = True)

You can also do comparisons. In the above case, we instead might simply want to identify regions
that are hotter than the global average. In that case we can simply do this:

.. code:: ipython3

    ds.assign(temp_comp = lambda x: x.temperature > spatial_mean(x.temperature), drop = True)

Let's say we wanted to map regions which are 3 degrees hotter than average. We could that as follows:

.. code:: ipython3

    ds.assign(temp_comp = lambda x: x.temperature > spatial_mean(x.temperature + 3), drop = True)

or like this:

.. code:: ipython3

    ds.assign(temp_comp = lambda x: x.temperature > (spatial_mean(x.temperature)+3), drop = True)

Logical operators work in the standard Python way. So if we had a dataset with a variable called 'var'
and we wanted to find cells with values between 1 and 10, we could do this:

.. code:: ipython3

    ds.assign(one2ten = lambda x: x.var > 1 & x.var < 10) 


You can process multiple variables at once using ``assign``. Variables
will be created in the order given, and variables created by the first
lambda function can be used by the next one, and so on. The simple
example below shows how this works. First we create a var1, which is
temperature plus 1. Then var2, which is var1 plus 1. Finally, we
calculate the difference between var1 and var2, and this should be 1
everywhere:

.. code:: ipython3

    ds.assign(var1 = lambda x: x.var + 1, var2 = lambda x: x.var1 + 1, diff = lambda x: x.var2 - x.var1)

Functions that work with nctoolkit variables
--------------------------------------------

The following functions can be used on nctoolkit variables as part of
lambda functions.

+-----------------------+-----------------------+--------------------------+
| Function              | Description           | Example                  |
+=======================+=======================+==========================+
| ``abs``               | Absolute value        | ``abs(x.sst)``           |
+-----------------------+-----------------------+--------------------------+
| ``ceiling``           | Ceiling of variable   | ``ceiling(x.sst -1)``    |
+-----------------------+-----------------------+--------------------------+
| ``cell_area``         | Area of grid-cell     | ``cell_area(x.var)``     |
|                       | (m2)                  |                          |
+-----------------------+-----------------------+--------------------------+
| ``cos``               | Trigonometric cosine  | ``cos(x.var)``           |
|                       | of variable           |                          |
+-----------------------+-----------------------+--------------------------+
| ``day``               | Day of the month of   | ``day(x.var)``           |
|                       | the variable          |                          |
+-----------------------+-----------------------+--------------------------+
| ``exp``               | Exponential of        | ``exp(x.sst)``           |
|                       | variable              |                          |
+-----------------------+-----------------------+--------------------------+
| ``floor``             | Floor of variable     |                          |
|                       |                       | ``floor(x.sst + 8.2)``   |
+-----------------------+-----------------------+--------------------------+
| ``hour``              | Hour of the day of    | ``hour(x.var)``          |
|                       | the variable          |                          |
+-----------------------+-----------------------+--------------------------+
| ``isnan``             | Is variable a missing | ``isnan(x.var)``         |
|                       | value/NA?             |                          |
+-----------------------+-----------------------+--------------------------+
| ``latitude``          | Latitude of the grid  | ``latitude(x.var)``      |
|                       | cell                  |                          |
+-----------------------+-----------------------+--------------------------+
| ``level``             | Vertical level of     | ``level(x.var)``         |
|                       | variable.             |                          |
+-----------------------+-----------------------+--------------------------+
| ``log``               | Natural log of        | ``log10(x.sst + 1)``     |
|                       | variable              |                          |
+-----------------------+-----------------------+--------------------------+
| ``log10``             | Base log10 of         | ``log10(x.sst + 1)``     |
|                       | variable              |                          |
+-----------------------+-----------------------+--------------------------+
| ``longitude``         | Longitude of the grid | ``longitude(x.var)``     |
|                       | cell                  |                          |
+-----------------------+-----------------------+--------------------------+
| ``month``             | Month of the variable | ``month(x.var)``         |
+-----------------------+-----------------------+--------------------------+
| ``sin``               | Trigonometric sine of | ``sin(x.var)``           |
|                       | variable              |                          |
+-----------------------+-----------------------+--------------------------+
| ``spatial_max``       | Spatial max of        |                          |
|                       | variable at time-step | ``spatial_max(x.var)``   |
+-----------------------+-----------------------+--------------------------+
| ``spatial_mean``      | Spatial mean of       |                          |
|                       | variable at time-step | ``spatial_mean(x.var)``  |
+-----------------------+-----------------------+--------------------------+
| ``spatial_min``       | Spatial min of        |                          |
|                       | variable at time-step | ``spatial_min(x.var)``   |
+-----------------------+-----------------------+--------------------------+
| ``spatial_sum``       | Spatial sum of        |                          |
|                       | variable at time-step | ``spatial_sum(x.var)``   |
+-----------------------+-----------------------+--------------------------+
| ``sqrt``              | Square root of        |                          |
|                       | variable              | ``sqrt(x.sst + 273.15)`` |
+-----------------------+-----------------------+--------------------------+
| ``tan``               | Trigonometric tangent | ``tan(x.var)``           |
|                       | of variable           |                          |
+-----------------------+-----------------------+--------------------------+
| ``timestep``          | Time step of          | ``timestep(x.var)``      |
|                       | variable. Using       |                          |
|                       | Python indexing.      |                          |
+-----------------------+-----------------------+--------------------------+
| ``year``              | Year of the variable  | ``year(x.var)``          |
+-----------------------+-----------------------+--------------------------+
| ``zonal_max``         | Zonal max of variable | ``zonal_max(x.var)``     |
|                       | at time-step          |                          |
+-----------------------+-----------------------+--------------------------+
| ``zonal_mean``        | Zonal mean of         | ``zonal_mean(x.var)``    |
|                       | variable at time-step |                          |
+-----------------------+-----------------------+--------------------------+
| ``zonal_min``         | Zonal min of variable | ``zonal_min(x.var)``     |
|                       | at time-step          |                          |
+-----------------------+-----------------------+--------------------------+
| ``zonal_sum``         | Zonal sum of variable | ``zonal_sum(x.var)``     |
|                       | at time-step          |                          |
+-----------------------+-----------------------+--------------------------+

Simple mathematical operations on variables
----------------------------------------------------

If you want to do simple operations like adding or subtracting numbers from the variables in datasets you can use
the ``add``, ``subtract``, ``divide`` and ``multiply`` methods. For example if you wanted to add 10 to every variable
in a dataset, you would do the following:

.. code:: ipython3

    ds.add(10)

If you wanted to multiply everything by 10, you would do this:

.. code:: ipython3

    ds.multiply(10)


These methods will also let you use other datasets or netCDF files. So, you could add the values in a dataset data2 to a dataset
called data1 as follows:


.. code:: ipython3

    ds1.add(ds2)


Please note that this will require that the datasets are structured in a way that the operation makes sense. So each dimension in the datasets
will either have to be identical, with the exception of when one dataset has a single value for a dimension. So for example if ds2 above has
data covering only 1 timestep, but ds1 has multiple timesteps the data from that single time step will be added to all timesteps in ds1.
But if the time steps match, then the data from the first time step in ds2 will be added to the data in the first time step in ds1, and the
same will happen with the following time steps.


Simple numerical comparisons 
----------------------------------------------------

If you want to do something as simple as working out whether the values of the variables in a dataset are greater than zero, you can use the 
``compare`` method. This method accepts a simple comparison formula, which follows Python conventions. For example, if you wanted to figure
out if the values in a dataset were greater than zero, you would do the following:

.. code:: ipython3

    ds.compare(">0")

If you wanted to know if they were equal to zero you would do this:

.. code:: ipython3

    ds.compare("==0")












