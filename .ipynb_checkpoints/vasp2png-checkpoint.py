from ase.io import read, write

atoms = read(CONTCAR)  # Read VASP file
write('side-view.png', atoms, rotation='-90x, -90y, 0z', show_unit_cell=0)  # Write PNG