from ase.io import read, write
from ase import Atoms

atoms = read('modified_structure.json')
atoms += Atoms('H', positions=[atoms[-1].position + (0.8, 0, 0.6)])

write('CONTCAR', atoms)
