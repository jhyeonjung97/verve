import os
from ase.io import read, write

# Read the atomic structure from the JSON file
atoms = read(f'{os.getcwd()}/0_/restart.json')

# Define the dz values to be added to the z-coordinate
dz = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

# Loop through the atoms
for atom in atoms:
    # Check if the atom symbol is not in the list ['C', 'N', 'O', 'H']
    if atom.symbol not in ['C', 'N', 'O', 'H']:
        # Loop through the dz list
        for i in range(6):
            # Update the z-coordinate of the atom
            atom.z = 10 + dz[i]
            # Write the modified atoms to a new JSON file
            write(f'restart{i+1}.json', atoms)
