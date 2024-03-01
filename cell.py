from ase import Atoms

# Create an example atoms object
atoms = Atoms('Si', cell=[[5.23987335, 0.0, 0.0], [4.366561618, 2.896448231, 0.0], [4.366561618, 1.316567459, 2.579934589]])

# Display the original cell parameters
print("Original Cell:")
print(atoms.cell)

# Define the scaling factor (adjust this value as needed)
scaling_factor = 0.95

# Scale the entire structure
atoms.set_cell(atoms.get_cell() * scaling_factor, scale_atoms=True)

# Display the modified cell parameters
print("\nModified Cell:")
print(atoms.cell)
