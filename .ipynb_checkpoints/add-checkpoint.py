from ase.io import read, write
from ase.atom import Atom

atoms = read('start.traj')
for atom in atoms:
    if atom.symbol == 'Mn':
        atoms.append(Atom('O', position=atom.position+(0,0,2.0)))
write('start.traj', atoms)