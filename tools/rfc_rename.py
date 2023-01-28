import json
import os

from pathlib import Path

# assign directory
directory = 'txt'

# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    filename = str(file)
    old_ext = filename.split(".")[1]
    new_ext = old_ext.split("_")[0]
    index = old_ext.split("_")[-1]
    new_filename = filename.split(".")[0] + '_' + index + '.' + new_ext
    os.rename(filename, new_filename)
    print(new_filename)