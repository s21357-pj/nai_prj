import json
import os

from pathlib import Path

# assign directory
directory = 'RFC-all'

# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    p = 0
    w_lines = []
    marked = False
    std = False
    print(file)
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'internet' in line:
                marked = True
            if 'Category: Standards Track' in line:
                std = True
        if marked and std:
            for line in lines:
                if '[Page' in line:
                    with open('rfc/' + str(file) + '_' + str(p), 'w') as f:
                        f.writelines(w_lines)
                    w_lines = []
                    p += 1
                w_lines.append(line)
    except Exception:
        pass
