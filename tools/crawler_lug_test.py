import json
import os

from pathlib import Path
import nltk

# assign directory
directory = 'lug'
new_lines = []
# iterate over files in
# that directory
files = Path(directory).glob('*')
for file in files:
    #print(file)
    writing = False
    new_lines = []
    pr = False
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line != '\n':
            if 'From:' in line:
                continue
            if '<blockquote>' in line:
                continue
            if '</blockquote>' in line:
                continue
            if 'To:' in line:
                continue
            if 'Cc:' in line:
                continue
            if 'Sent:' in line:
                continue
            if 'Subject:' in line:
                continue
            if '--' in line:
                continue
            if 'http:' in line:
                continue
            if 'date:' in line.lower():
                continue
            if 'wrote' in line:
                continue
            if 'https:' in line:
                continue
            if '@' in line:
                continue
            if 'pgp' in line.lower() and 'key' in line.lower():
                continue
            if ' attachment ' in line.lower():
                continue
            if 'mailto' in line.lower():
                continue
            if len(nltk.word_tokenize(line)) < 4:
                continue
        new_lines.append(line)
    #print(new_lines)
    with open(file, 'w') as f:
        f.writelines(new_lines)

