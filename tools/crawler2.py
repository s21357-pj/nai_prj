import json
import os

import wikipedia
from pathlib import Path

# assign directory
directory = 'crawled_files'

# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    print(file)
    with open(file, 'r') as f:
        data = json.load(f)
    with open('txt/' + str(file).replace('json',
                                         'txt'), 'w') as f:
        f.write(data["content"])
