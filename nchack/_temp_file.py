import tempfile

def temp_file(ext = ""):

            target = tempfile.NamedTemporaryFile().name 
            target = target.replace("tmp/", "tmp/nchack")
            target = target + ".nc"
            return target



