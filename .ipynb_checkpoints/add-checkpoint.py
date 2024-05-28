from ase.io import read, write
from ase import Atoms
from ase.atom import Atom

atoms = read('start.traj')

for atom in atoms:
    if atom.symbol == 'Mn':
        p = atom.position
    elif atom.symbol == 'O' and atom.position[2] < p[2]:
        # atoms.append(Atom('H', position=atom.position + (+0.8, 0.0, +0.6)))
        atoms.append(Atom('H', position=atom.position + (-0.8, 0.0, -0.6)))

write('start.traj', atoms)
