from ase.io import read, write
from ase import Atoms

# Read the atomic structure from the JSON file
atoms = read('moments.json')

# Get the magnetic moments of the atoms
magmoms = atoms.get_magnetic_moments()

# Initialize a list to store new atoms and their magnetic moments
new_atoms = []
new_magmoms = list(magmoms)

# Add oxygen atoms 2.0 Å above each non-C, N, O, H atom
for atom in atoms:
    if atom.symbol not in ['C', 'N', 'O', 'H']:
        new_atom = Atoms('O', positions=[atom.position + (0, 0, 2.0)])
        new_atoms.append(new_atom)
        new_magmoms.append(5)

# Add the new atoms to the original atoms object
for new_atom in new_atoms:
    atoms += new_atom

# Set the initial magnetic moments
atoms.set_initial_magnetic_moments(new_magmoms)

# Write the modified structure with oxygen atoms to a JSON file
write('modified_structure_o.json', atoms)

# Add a hydrogen atom 0.8 Å along x and 0.6 Å along z from the last atom's position
last_atom_position = atoms[-1].position
new_h_atom = Atoms('H', positions=[last_atom_position + (0.8, 0, 0.6)])
atoms += new_h_atom

# Update the magnetic moments list and set it again
new_magmoms.append(5)
atoms.set_initial_magnetic_moments(new_magmoms)

# Write the final modified structure with the added hydrogen atom to another JSON file
write('modified_structure_h.json', atoms)
