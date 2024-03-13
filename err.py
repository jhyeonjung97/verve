import re

pattern = re.compile(r'--------------')
# error_found = False
with open('./vasp.out', 'r') as file:
    for line in file:
        if pattern.search(line):
            print('Warning: Error found in any vasp.out files.')
            # error_found = True
            break