from ase.io import read, write
from ase.atom import Atom

atoms = read('CONTCAR')
for atom in atoms:
    if atom.symbol == 'Mn':
        atoms.append(Atom('O', position=atom.position+(0.0,0.0,-1.8)))
write('start.traj', atoms)