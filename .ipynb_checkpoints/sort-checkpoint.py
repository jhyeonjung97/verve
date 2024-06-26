from ase.io import read, write
from ase import Atoms

def main(input_file, output_file):
    # Read the POSCAR file
    atoms = read(input_file, format='vasp')
    
    # Separate metals and oxygens
    metal_atoms = [atom for atom in atoms if atom.symbol != 'O']
    oxygen_atoms = [atom for atom in atoms if atom.symbol == 'O']
    
    # Combine sorted atoms: metals first, then oxygens
    sorted_atoms = metal_atoms + oxygen_atoms
    
    # Create a new Atoms object with the sorted atoms
    sorted_atoms_obj = Atoms([atom for atom in sorted_atoms],
                             cell=atoms.get_cell(),
                             pbc=atoms.get_pbc())
    
    # Write the sorted atoms back to a POSCAR file
    write(output_file, sorted_atoms_obj, format='vasp')
    print(f"Sorted POSCAR file has been saved as {output_file}")

if __name__ == "__main__":
    input_file = 'POSCAR'  # Replace with your input file name
    output_file = 'POSCAR_sorted'  # Replace with your desired output file name
    main(input_file, output_file)
