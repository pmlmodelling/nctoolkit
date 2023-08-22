import os
import warnings


def reset(self):
    """
    Simple method to fully reset a datset

    """

    self.current = self._start
    self._execute = False
    self._history = []
    self._hold_history = []
    self._merged = False
    self_safe = []
    if os.path.exists(self[0]):
        self._thredds = False
    else:
        self._thredds = True
    self_zip = False
    self_format = None
    self._precision = "default"
    self._grid = None
    self._weights = None
    self._ncommands = 0
    warnings.warn(
        "The dataset has been reset to the starting point due to a run failure! Please change commands, where applicable, and re-run."
    )

    # if files have been removed, we need to reset the attributes
    self._atts["variables"] = [None, -1]
    self._atts["months"] = [None, -1]
    self._atts["levels"] = [None, -1]
    self._atts["times"] = [None, -1]
    self._atts["calendar"] = [None, -1]
    self._atts["size"] = [None, -1]
    self._atts["ncformat"] = [None, -1]
    self._atts["years"] = [None, -1]
    self._atts["calendar"] = [None, -1]
    self._atts["contents"] = [None, -1]
