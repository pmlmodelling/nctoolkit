import tempfile
import os


from ._session import session_stamp

def temp_file(ext = ""):

        # check space left in temp dir and switch it if there isn't much
        if session_stamp["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result <  0.5 * 1e9:
                if session_stamp["temp_dir"] == "/tmp/":
                    session_stamp["temp_dir"] = "/var/tmp/"

            actual_temp = session_stamp["temp_dir"]
            actual_temp = actual_temp + "/"
            actual_temp = actual_temp.replace("//", "/")

            target = tempfile.NamedTemporaryFile().name 
            target = target.replace("tmp/", "tmp/" + session_stamp["stamp"])
            target = target.replace("tmp/", "tmp/" + session_stamp["stamp"])
            #if actual_temp != "/tmp/":
            target = actual_temp + os.path.basename(target)
            target = target + ".nc"
            return target



