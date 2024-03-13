import re

pattern = re.compile(r'--------------')
with open('./vasp.out', 'r') as file:
    for line in file:
        if pattern.search(line):
            print('Warning: Error found in any vasp.out files.')
            break