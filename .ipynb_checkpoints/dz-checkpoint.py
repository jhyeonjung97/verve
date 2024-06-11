from ase.io import read
from statistics import mean


atoms = read('CONTCAR')

zN = mean([atom.z for atom in atoms if atom.symbol == 'N'])
zM = mean([atom.z for atom in atoms if atom.symbol != 'N' and atom.symbol != 'O' and atom.symbol != 'H'])
print(zN)
print(zM)
dz = abs(zN - zM)*20
print(dz)