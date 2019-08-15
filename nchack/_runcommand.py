import os

def run_command(os_command):
    """ Function to run an nco/cdo system command and check output was generated"""

    # Step 1: find the output file that is being created

    out_file = os_command.split(" ")
    out_file = out_file[-1]

    # Step 2: run the system command

    os.system(os_command)
    
    # Step 3: check the file was actually created
    # Raise error if it wasn't

    if os.path.exists(out_file) is False:
        raise ValueError(run_command, " was not successful. Check output")
