
import os

def view(self):
    if type(self.current) is str:
        os.system("ncview " + self.current + "&")
    else:
        print("You cannot send multiple files to ncview!")

