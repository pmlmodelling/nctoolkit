import tempfile
import os


from ._session import session_stamp

def temp_file(ext = ""):

            actual_temp = session_stamp["temp_dir"]
            actual_temp = actual_temp + "/"
            actual_temp = actual_temp.replace("//", "/")

            target = tempfile.NamedTemporaryFile().name 
            target = target.replace("tmp/", "tmp/" + session_stamp["stamp"])
            target = target.replace("tmp/", "tmp/" + session_stamp["stamp"])
            if actual_temp != "/tmp/":
                target = actual_temp + os.path.basename(target)
            target = target + ".nc"
            return target



