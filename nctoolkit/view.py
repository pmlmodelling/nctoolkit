
import os

def view(self):
    """
    Open the current dataset's file in ncview
    """
    self.run()

    if type(self.current) is str:
        os.system("ncview " + self.current + "&")
    else:
        print("You cannot send multiple files to ncview!")
