from ase.io import read, write
from ase import Atoms
from ase.atom import Atom

# Read the initial atomic structure from 'start.traj'
atoms = read('start.traj')

# Preserve cell information
cell = atoms.get_cell()
pbc = atoms.get_pbc()

# Create a new list excluding O and H atoms
filtered_atoms = [atom for atom in atoms if atom.symbol not in ['O', 'H']]

# List to hold new atoms
new_atoms = []

# Add new atoms around Mn atoms
for atom in filtered_atoms:
    if atom.symbol == 'Mn':
        new_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, +1.8)))
        new_atoms.append(Atom('O', position=atom.position + (0.0, 0.0, -1.8)))
        new_atoms.append(Atom('H', position=atom.position + (0.0, 0.0, +1.8) + (+0.8, 0.0, +0.6)))
        # Uncomment the following line if you want to add this hydrogen atom as well
        # new_atoms.append(Atom('H', position=atom.position + (0.0, 0.0, -1.8) + (-0.8, 0.0, -0.6)))

# Combine the filtered_atoms and new_atoms into one Atoms object, preserving cell info
combined_atoms = Atoms(filtered_atoms + new_atoms, cell=cell, pbc=pbc)

# Write the modified structure to 'start.traj'
write('hello.traj', combined_atoms)
