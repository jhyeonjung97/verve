from ase.io import read, write
from ase.atom import Atom

# Read the initial atomic structure from 'start.traj'
atoms = read('start.traj')

# Create a new list excluding O and H atoms
atoms = [atom for atom in atoms if atom.symbol not in ['O', 'H']]

# List to hold new atoms
new_atoms = []

# Add new atoms around Mn atoms
for atom in atoms:
    if atom.symbol == 'Mn':
        new_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, +1.8)))
        new_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, -1.8)))
        new_atoms.append(Atom('H', position=atom.position + (0.0, 0.0, +1.8) + (+0.8, 0.0, +0.6)))
        # Uncomment the following line if you want to add this hydrogen atom as well
        # new_atoms.append(Atom('H', position=atom.position + (0.0, 0.0, -1.8) + (-0.8, 0.0, -0.6)))

# Extend the atoms list with new atoms
atoms.extend(new_atoms)

# Write the modified structure to 'start.traj'
write('hello.traj', atoms)
