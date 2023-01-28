import json
import os

from pathlib import Path

# assign directory
directory = 'rfc/RFC-all'

# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    #print(file)
    writing = False
    new_lines = []
    pr = False
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if writing:
                new_lines.append(line)
            if 'January' in line:
                writing = True
            if 'February' in line:
                writing = True
            if 'March' in line:
                writing = True
            if 'April' in line:
                writing = True
            if 'May' in line:
                writing = True
            if 'June' in line:
                writing = True
            if 'July' in line:
                writing = True
            if 'August' in line:
                writing = True
            if 'September' in line:
                writing = True
            if 'October' in line:
                writing = True
            if 'November' in line:
                writing = True
            if 'December' in line:
                writing = True

    except Exception:
        os.remove(file)
    with open(file, 'w') as f:
        f.writelines(new_lines)

