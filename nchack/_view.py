
import os

def to_ncview(self):
    if type(self.current) is str:
        os.system("ncview " + self.current)
    else:
        print("You cannot send multiple files to ncview!")

