from ase.io import read, write
from ase.build import sort
from sys import argv
import os

if not argv[2]:
    print('wrong usage: convert (type1) (type2) [lattice]')
    exit()

for file in os.listdir('./'):
    if file.endswith('.%s' %argv[1]):
        atoms = read(file)
        write(file.replace('%s' %argv[1], '%s' %argv[2]), atoms, format='%s' %argv[2])
    else:
        continue