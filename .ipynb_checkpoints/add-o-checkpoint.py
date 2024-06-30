from ase.io import read, write
from ase import Atoms

atoms = read('restart.json')
for atom in atoms:
    if atom.symbol not in ['C', 'N', 'O', 'H']:
        atoms += Atoms('O', positions=[atom.position + (0, 0, 2.0)])

write('modified_structure.json', atoms)
