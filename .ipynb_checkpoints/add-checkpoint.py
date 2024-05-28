from ase.io import read, write
from ase.atom import Atom

atoms = read('start.traj')
del atoms[[atom.index for atom in atoms if atom.symbol=='O']]
for atom in atoms:
    if atom.symbol == 'Mn':
        atoms.append(Atom('O', position=atom.position+(0.0,0.0,+1.8)))
        atoms.append(Atom('O', position=atom.position+(0.0,0.0,-1.8)))
        atoms.append(Atom('H', position=atom.position+(0.0,0.0,+1.8)+(+0.8,0.0,+0.6)))
        atoms.append(Atom('H', position=atom.position+(0.0,0.0,-1.8)+(-0.8,0.0,-0.6)))
write('start.traj', atoms)