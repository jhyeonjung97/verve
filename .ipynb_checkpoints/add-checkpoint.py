from ase.io import read, write
from ase import Atoms
from ase.atom import Atom

atoms = read('start.traj')
filtered_atoms = [atom for atom in atoms if atom.symbol not in ['O', 'H']]

for atom in filtered_atoms:
    if atom.symbol == 'Mn':
        filtered_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, +1.8)))
        filtered_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, -1.8)))
        filtered_atoms.append(Atom('H', position=atom.position + (0.0, 0.0, +1.8) + (+0.8, 0.0, +0.6)))
        break
        # atoms.append(Atom('H', position=atom.position + (0.0, 0.0, -1.8) + (-0.8, 0.0, -0.6)))

write('hello.traj', filtered_atoms)
