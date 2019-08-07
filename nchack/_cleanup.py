
import os
import sys

from ._filetracker import nc_created

# keep is a file you do not want to delete

def cleanup(keep = None):
    candidates = [x for x in nc_created if os.path.exists(x)]
    candidates = set(candidates)
    candidates = list(candidates)
    
    
    # Step 2 is to find the trackers in the locals
    
    valid_files = []
    objects = dir(sys.modules["__main__"])
    for i in ([v for v in objects if not v.startswith('_')]):
        i_class = str(eval("type(sys.modules['__main__']." +i + ")"))
        if "NCTracker" in i_class:
            i_current =eval("sys.modules['__main__']." +i + ".current")
            i_start =eval("sys.modules['__main__']." +i + ".start")
            if i_current != i_start:
                valid_files.append(i_current)
                print(i_current)
    
    delete_these = [v for v in candidates if v not in valid_files]            
    if keep is not None:
        delete_these = [v for v in delete_these if v != keep]            

    delete_these = set(delete_these)
    delete_these = list(delete_these)

    
    for dd in delete_these:
        os.remove(dd)
        print(dd)
    
