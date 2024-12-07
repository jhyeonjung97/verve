import os
from ase.io import read, write

for vasp_file in os.listdir('.'):  # List all files in the current directory
    if vasp_file.endswith('.vasp'):  # Process only files with .vasp extension
        atoms = read(vasp_file)  # Read VASP file
        atoms = atoms.repeat((3,3,1))
        filename = os.path.splitext(vasp_file)[0]  # Get the filename without extension
        png_file = f"{filename}.png"  # Define output PNG filename
        write(png_file, atoms, rotation='0x, 0y, 0z', show_unit_cell=0)  # Write PNG
