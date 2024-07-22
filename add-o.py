from ase.io import read, write
from ase import Atoms

# Read the atomic structure from the JSON file
atoms = read('moments.json')

# Get the magnetic moments of the atoms
magmoms = atoms.get_magnetic_moments()

# Assign magnetic moments and add oxygen atoms
for atom in atoms:
    atom.magmom = magmoms[atom.index]
    if atom.symbol not in ['C', 'N', 'O', 'H']:
        # Add an oxygen atom 2.0 Å above the current atom
        atoms += Atoms('O', positions=[atom.position + (0, 0, 2.0)], initial_magmom=0)

# Write the modified structure with oxygen atoms to a JSON file
write('modified_structure_o.json', atoms)

# Add a hydrogen atom 0.8 Å along x and 0.6 Å along z from the last atom's position
atoms += Atoms('H', positions=[atoms[-1].position + (0.8, 0, 0.6)], initial_magmom=0)

# Write the final modified structure with the added hydrogen atom to another JSON file
write('modified_structure_h.json', atoms)
