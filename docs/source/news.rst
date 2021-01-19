News
============

Release of v0.3.0 
---------------

Version 0.3.0 will be released in February 2021. This will be a major release introducing major improvements to the package.

A new method ``assign``  is now available for generating new variables. This replaces the ``mutate`` and ``transmute``, which were 
place-holder functions in the early releases of nctoolkit until a proper method for creating variables was put in place.
``assign`` operates in the same way as the ``assign`` method in Pandas. Users can generate new variables using lambda functions.

This release will also allow users to run nctoolkit in parallel. Previous releases allowed files in multi-file datasets to be 
processed in parallel. However, it was not possible to create processing chains and process files in parallel. This is now possible
in version thanks to under-the-hood changes in nctoolkit's code base.

Users are now able to add a configuration file, which means global settings do not need to be set in every session or in every script.





