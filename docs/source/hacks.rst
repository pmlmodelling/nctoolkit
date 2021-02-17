Random Data Hacks
------------------

nctoolkit features a number of useful methods to tweak data.


Shifting time
================

Sometimes the times in datasets are not quite what we want, and we need some way to adjust time. An example of this
is when you are missing a year of data, so want to copy data from the prior year and use it. But first you would need
to shift the times in that year forward by a year. You can do this with the ``shift`` method. This let's you shift
time forward by a specified number of hours, days, months or years. You just need to supply hours, days, months or years
as an argument. So, if you wanted to shift time backward by one year, you would do the following:

.. code:: ipython3

    data.shift(years = -1)

If you wanted to shift time forward by 12 hours, this would do it:


.. code:: ipython3

    data.shift(hours = 12)

Note: this method allows partial matches to the arguments, so you could use hour, day, month or year just as easily. 



