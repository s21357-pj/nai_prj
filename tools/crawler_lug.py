import json
import os

from pathlib import Path
import nltk
from nltk.corpus import wordnet

def check_sentence(line):
    n = 0
    for word in nltk.word_tokenize(line):
        if wordnet.synsets(word):
            n += 1
    return n

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
    try:
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
                if 'from' in line.lower() and 'at' in line.lower():
                    continue
                if 'at nanog.org' in line.lower():
                    continue
                if '.png' in line.lower():
                    continue
                if '.jpg' in line.lower():
                    continue
                if '.jpeg' in line.lower():
                    continue
                if '.gif' in line.lower():
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
                if check_sentence(line) < 4:
                    continue
            new_lines.append(line)
            # print(new_lines)
        with open(file, 'w') as f:
            f.writelines(new_lines)
    except Exception:
        os.remove(file)


