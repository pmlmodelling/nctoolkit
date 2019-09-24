
import os


def convert_bytes(num):
    """
     A function to make file size human readable
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1000.0:
            return str(num) + " " + x 
        num /= 1000.0


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size



def size(self):
    """Method to calculate the size of a tracker"""

    if type(self.current) is str:
        result = "Number of files: 1\n"
        result = result + "File size: " + convert_bytes(file_size(self.current))
        print(result)
    else:
        all_sizes = []
        
        smallest_file = ""
        largest_file = ""
        min_size = 1e15 
        max_size = -1 

        for ff in self.current:

            all_sizes.append(file_size(ff))

            if file_size(ff) > max_size:
                max_size = file_size(ff)
                largest_file = ff

            if file_size(ff) < min_size:
                min_size = file_size(ff)
                smallest_file = ff

        min_size = convert_bytes(min_size)
        max_size = convert_bytes(max_size)

        sum_size = convert_bytes(sum(all_sizes))
        result = "Number of files in ensemble: " + str(len(self.current)) + "\n"
        result = result + "Ensemble size: " + sum_size  + "\n"
        result = result + "Smallest file " + smallest_file + " has size "  + min_size  + "\n"
        result = result + "Largest file " + largest_file + " has size "  + max_size 
        print(result)



