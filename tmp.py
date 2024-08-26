import os
import glob
import numpy as np
from ase.io import read, write
from ase.build import surface
from ase.build.tools import sort
from ase.build import make_supercell, cut
from ase.constraints import FixAtoms
from ase.geometry.geometry import get_duplicate_atoms
from ase.io.vasp import read_vasp_xdatcar, write_vasp_xdatcar

pattern = os.path.join('./', f'1*.vasp')
matching_files = glob.glob(pattern)
for file in matching_files:
    atoms = read(f'{file}')
    displacement = atoms[0].position
    atoms.translate(displacement+[0,0,0.1])
    atoms.wrap()
    atoms.center()
    get_duplicate_atoms(atoms, cutoff=0.1, delete=True)
    write(f'{file}',atoms)