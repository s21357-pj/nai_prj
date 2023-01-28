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
    try:
        data["content"] = wikipedia.page(
            data["meta"]["url"].replace("https://en.m.wikipedia.org/wiki/",
                                        "")).content
        data["content"] = data["content"].replace("\n", " ")

        if 'operatorname' in data["content"]:
            raise Exception
        with open(file, 'w') as f:
            json.dump(data, f)
        
    except Exception:
        os.remove(file)
