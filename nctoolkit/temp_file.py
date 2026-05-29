import os
import tempfile

from nctoolkit.session import session_info
from nctoolkit.session import append_tempdirs


def temp_file(ext=""):
    """
    Function to create a temporary file.
    This accounts for OS

    Parameters
    --------------------
    ext : str
        File extension
    """

    # check space left in temp dir and switch it if there isn't much
    if session_info["temp_dir"] == "/tmp/":
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail

        if result < 0.5 * 1e9:
            if session_info["temp_dir"] == "/tmp/":
                session_info["temp_dir"] = "/var/tmp/"

    actual_temp = session_info["temp_dir"]
    actual_temp = actual_temp + "/"
    actual_temp = actual_temp.replace("//", "/")

    target = tempfile.NamedTemporaryFile().name
    target = target.replace("tmp/", "tmp/" + session_info["stamp"])

    target = actual_temp + os.path.basename(target)
    if not isinstance(ext, str):
        raise TypeError("Extension supplied is not a str")
    if ext.startswith("."):
        target = target + ext
    else:
        target = f"{target}.{ext}"

    append_tempdirs(os.path.dirname(target))

    return target

