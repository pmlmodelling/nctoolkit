Contributing to nctoolkit
=============================

We welcome contributions to nctoolkit! The following are all welcome contributions:

- Bug reports
- Bug fixes
- New features
- New documentation
- New examples
- New tutorials
- New tests

Right now nctoolkit is developed by marine scientists, and we would love to have more input from other fields. 
In particular, we would love to have more input from the atmospheric sciences community. If you are interested in contributing, please reach out to us!


Report bugs using Github's issues
---------------------------------

We track bugs using Github's issues. If you have found a bug, please open an issue.

If you do raise an issue try to do the following:

- Check if the issue has already been raised
- Check if the issue has already been fixed in the latest code
- Create a reproducible example that demonstrates the problem
- Specify the operating system you are using and Python version 
- Specify the version of nctoolkit you are using

If you are able to fix the bug yourself, please open a pull request with the fix.

The developers will try to respond to issues as quickly as possible, but please be patient.



-------------------------------------------------------------------

Pull requests are the best way to propose changes to the codebase (we use Github Flow). We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

All contributions you make will be under the GNU General Public License v3.0 
----------------------------------------------------------------

When you submit code changes, your submissions are understood to be under the same [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/) that covers the project. Feel free to contact the maintainers if that's a concern.

As stated in the license, we are not liable for any damages that may arise from your use of the code. Read the full license [here](https://choosealicense.com/licenses/gpl-3.0/).


How to suggest a feature or enhancement or contribute code
---------------------------------------

Our preferred work flow for suggesting a new feature is to first either open an issue or a new discussion on Github. 
This allows us to discuss the feature before you spend time writing code.
If you are interested in contributing, please reach out to us! We are happy to help you get started. It is best to start by either opening an issue or a new discussion on Github. This allows us to discuss the feature before you spend time writing code.  

If you have already written code, please open a pull request.

Naturally, the best way to get your feature accepted is to write it yourself. 
When you are ready to write code, please follow the following steps:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

We will try to respond to pull requests as quickly as possible, but please be patient.

A note on nctoolkit methods
---------------------------------------

In general dataset methods do one of two things: modifying datasets or analyzing datasets. Analysis will include things such as plotting. 

As explained in the documentation, methods should be as lazy as possible. This allows nctoolkit to chain CDO commands together and prevents unnecessary I/O.

Ideally, method code will either call CDO using the `cdo_command` method or use existing nctoolkit methods. 

If you want to get started with the API a good place to start is the `fill_na` method.


.. code-block:: python

  def fill_na(self, n=1):
      """
      Fill missing values with a distance-weighted average. This carries out infilling for each time step and vertical level.

      Parameters
      -------------
      n: int
          Number of nearest neighbours to use. Defaults to 1. To
      """

      cdo_command = f"cdo -setmisstodis,{n}"

      self.cdo_command(command=cdo_command, ensemble=False)


This method fills missing values using distance weighting. The CDO call is equivalent of the following::

  $ cdo -setmisstodis,n input.nc output.nc

where n is the number of nearest neighbours to use. If the method you are considering writing can be implemented using CDO, then it is best to use CDO under the hood.

If you are unfamiliar with CDO, it is best to look through their excellent `user guide  <https://code.mpimet.mpg.de/projects/cdo/embedded/cdo.pdf>`__

At present, there are many methods in CDO that have yet to be implemented in nctoolkit. This includes EOFs and trend analysis. 
If you use CDO and nctoolkit and you feel something exists in CDO that should be in nctoolkit, reach out or open an issue.

Alternatively, if you want to implement a method that uses NCO you can do so using the `nco_command` method. 
In effect, nctoolkit is capable of doing anything CDO or NCO can. So there are many opportunities to contribute. 


