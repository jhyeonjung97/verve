from ase.io import read, write
from ase.atom import Atom

# Read the initial atomic structure from 'start.traj'
atoms = read('start.traj')

# Create a new list excluding O and H atoms
atoms = [atom for atom in atoms if atom.symbol not in ['O', 'H']]

# Add new atoms around Mn atoms
for atom in atoms:
    if atom.symbol == 'Mn':
        atoms.append(Atom('O', position=atom.position + (0.0, 0.0, +1.8)))
        atoms.append(Atom('O', position=atom.position + (0.0, 0.0, -1.8)))
        atoms.append(Atom('H', position=atom.position + (0.0, 0.0, +1.8) + (+0.8, 0.0, +0.6)))
        # atoms.append(Atom('H', position=atom.position + (0.0, 0.0, -1.8) + (-0.8, 0.0, -0.6)))

# Write the modified structure to 'start.traj'
write('start.traj', atoms)
