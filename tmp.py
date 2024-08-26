import os
import glob
import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.build import surface
from ase.build.tools import sort
from ase.build import make_supercell, cut
from ase.constraints import FixAtoms
from ase.geometry.geometry import get_duplicate_atoms
from ase.io.vasp import read_vasp_xdatcar, write_vasp_xdatcar

pattern = os.path.join('./', '7*.vasp')
matching_files = glob.glob(pattern)
for file in matching_files:
    print(file)
    atoms = read(f'{file}')
    
    # displacement = [0, 0, atoms[0].position[2]-0.1]
    cell = atoms.get_cell()
    # displacement = atoms[0].position
    displacement = [0, 0, cell[0, 0] / 2]
    atoms.positions -= displacement
    # atoms.positions += [0.1, 0.1, 0.1]
    atoms.wrap()
    atoms.center()
    get_duplicate_atoms(atoms, cutoff=0.1, delete=True)
    
    # indice = []
    # for atom in atoms:
    #     # if atom.z < 0.1:
    #     # if atom.symbol != 'O' and atom.index > 7:
    #     if atom.symbol == 'O' and atom.z > atoms[7].z + 0.5:
    #         indice.append(atom.index)
    # indice.reverse()
    # print(indice)
    # for index in indice:
    #     del atoms[index]

    # metal_atoms = [atom for atom in atoms if atom.symbol != 'O']
    # oxygen_atoms = [atom for atom in atoms if atom.symbol == 'O']
    # sorted_atoms = metal_atoms + oxygen_atoms
    # sorted_atoms_obj = Atoms([atom for atom in sorted_atoms],
    #                          cell=atoms.get_cell(),
    #                          pbc=atoms.get_pbc())
    
    write(f'{file}',atoms)
    # write(f'{file}',sorted_atoms_obj)