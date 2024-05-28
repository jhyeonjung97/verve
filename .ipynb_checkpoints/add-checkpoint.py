from ase.io import read, write
from ase import Atoms
from ase.atom import Atom

atoms = read('start.traj')

for atom in atoms:
    if atom.symbol=='O' or atom.symbol=='H': 
        del atom

print(atoms)

for atom in atoms:
    if atom.symbol == 'Mn':
        atoms.append(Atom('O', position=atom.position + (0.0, 0.0, +1.8)))
        atoms.append(Atom('O', position=atom.position + (0.0, 0.0, -1.8)))
        atoms.append(Atom('H', position=atom.position + (0.0, 0.0, +1.8) + (+0.8, 0.0, +0.6)))
        break
        # atoms.append(Atom('H', position=atom.position + (0.0, 0.0, -1.8) + (-0.8, 0.0, -0.6)))

write('hello.traj', atoms)
