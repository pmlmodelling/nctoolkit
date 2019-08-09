
An in development Python package to manipulate netcdf files.

Goals

# What it is not

Fundamentally, this package does not provide a full interface to all of the options available within CDO and NCO. Instead, this package aims to provide functionality that will cover 80-90% of the use cases when manipulating netcdf files. This will naturally involve some judgement and will be influenced by current work needs.


# System requirements
This will require both CDO and NCO to be installed on your computer. At present the package will not work on Windows because I have not had time to rewrite the system calls.

## Introducing trackers

The fundamental object of analysis in this package is a tracker. This object will store the start point of any manipulations. This will either be a single file or an ensemble of files. It will also store the current position of the manipulations. This is a single netcdf file stored in a temporary folder. In a similar vein, the package will track the history of manipulations on the terminal or within Python.


## Methods supported

TBC
