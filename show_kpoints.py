from ase.io import read
from sys import argv
import numpy as np

file = argv[1]
atoms = read(file)
l = 25
cell = atoms.get_cell()
nkx = int(round(l/np.linalg.norm(cell[0]),0))
nky = int(round(l/np.linalg.norm(cell[1]),0))
nkz = int(round(l/np.linalg.norm(cell[2]),0))
print(nkx, nky, nkz)