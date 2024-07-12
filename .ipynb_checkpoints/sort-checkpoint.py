from ase.io import read, write
from ase import Atoms

def main(input_file, output_file):
    # Read the POSCAR file
    atoms = read(input_file, format='vasp')
    
    # Separate metals and oxygens
    # lanthanum_atoms = [atom for atom in atoms if atom.symbol != 'O']
    metal_atoms = [atom for atom in atoms if atom.symbol != 'O']
    oxygen_atoms = [atom for atom in atoms if atom.symbol == 'O']
    
    # Combine sorted atoms: metals first, then oxygens
    sorted_atoms = metal_atoms + oxygen_atoms
    
    # Create a new Atoms object with the sorted atoms
    sorted_atoms_obj = Atoms([atom for atom in sorted_atoms],
                             cell=atoms.get_cell(),
                             pbc=atoms.get_pbc())
    
    # Transfer constraints from the original atoms object
    if atoms.constraints:
        sorted_atoms_obj.set_constraint(atoms.constraints)
    
    # Get the position of the first atom
    first_atom_position = sorted_atoms_obj.positions[0]
    
    # Calculate the center of the x and y axes of the unit cell
    cell = sorted_atoms_obj.get_cell()
    center_x = cell[0, 0] / 2
    center_y = cell[1, 1] / 2
    
    # Calculate the displacement to move the first atom to the center of the x and y axes
    displacement = [-first_atom_position[0], -first_atom_position[1], 0]
    # displacement = [center_x - first_atom_position[0], center_y - first_atom_position[1], 0]
    
    # Apply the displacement to all atoms
    # sorted_atoms_obj.translate(displacement)
    sorted_atoms_obj.wrap()
    sorted_atoms_obj.center()

    # Write the sorted and shifted atoms back to a POSCAR file
    write(output_file, sorted_atoms_obj, format='vasp')
    print(f"Sorted and shifted POSCAR file has been saved as {output_file}")

if __name__ == "__main__":
    input_file = 'POSCAR_xcell'  # Replace with your input file name
    output_file = 'POSCAR_sorted'  # Replace with your desired output file name
    main(input_file, output_file)
