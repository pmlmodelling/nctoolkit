import tempfile


from ._session import session_stamp

def temp_file(ext = ""):

            target = tempfile.NamedTemporaryFile().name 
            target = target.replace("tmp/", "tmp/" + session_stamp["stamp"])
            target = target + ".nc"
            return target



