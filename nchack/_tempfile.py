import tempfile

def temp_file():

            target = tempfile.NamedTemporaryFile().name 
            target = target.replace("tmp/", "tmp/nchack")



