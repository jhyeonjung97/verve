from ase.io import read, write
from ase.atom import Atom

atoms = read('start.traj')
for atom in atoms:
    if atom.symbol == 'O':
        atoms.append(Atom('H', position=atom.position+(0.8,0.0,0.6)))
write('start.traj', atoms)