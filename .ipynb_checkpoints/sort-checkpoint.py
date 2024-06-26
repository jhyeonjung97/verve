from ase.io import read, write

def main(input_file, output_file):
    # Read the POSCAR file
    atoms = read(input_file, format='vasp')
    
    # Separate metals and oxygens
    metal_atoms = [atom for atom in atoms if atom.symbol != 'O']
    oxygen_atoms = [atom for atom in atoms if atom.symbol == 'O']
    
    # Combine sorted atoms: metals first, then oxygens
    sorted_atoms = metal_atoms + oxygen_atoms
    
    # Create a new Atoms object with the sorted atoms
    sorted_atoms_obj = atoms.copy()
    sorted_atoms_obj.set_positions([atom.position for atom in sorted_atoms])
    sorted_atoms_obj.set_chemical_symbols([atom.symbol for atom in sorted_atoms])
    
    # Write the sorted atoms back to a POSCAR file
    write(output_file, sorted_atoms_obj, format='vasp')
    print(f"Sorted POSCAR file has been saved as {output_file}")

if __name__ == "__main__":
    input_file = 'POSCAR'  # Replace with your input file name
    output_file = 'POSCAR_sorted'  # Replace with your desired output file name
    main(input_file, output_file)
