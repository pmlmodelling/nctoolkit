import os

def run_command(os_command, target):
    """ Function to run an nco/cdo system command and check output was generated"""
    run = target.run

    # Step 1: find the output file that is being created

    out_file = os_command.split(" ")
    out_file = out_file[-1]
    print(out_file)

    # Step 2: run the system command

    if run:
        os.system(os_command)
        
        # Step 3: check the file was actually created
        # Raise error if it wasn't

        if os.path.exists(out_file) == False:
            raise ValueError(os_command + " was not successful. Check output")
    else:
        # Now, if this is not a cdo command we need throw an error

        if os_command.strip().startswith("cdo") == False:
            raise ValueError("You can only use cdo commands in hold mode")
        # Now, we need to throw an error if the command is generating a grid
        
        commas = [x for x in os_command.split(" ") if "," in x]
        commas = "".join(commas)
        if "gen" in commas:
            raise ValueError("You can generate weights as part of a chain!")



