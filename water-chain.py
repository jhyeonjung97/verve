import os
import numpy as np
from sys import argv
from ase import Atoms
from ase.io import read, write

def main():
    file = argv[1]
    atoms = read(file)
    name, ext = os.path.splitext(file)
    longest_chain = water_chain(atoms, 8)
    print(longest_chain)
    
    # new_dex = []
    # for i in longest_chain:
    #     for atom in atoms:
    #         if atom.symbol == 'H' and 0.5 < np.linalg.norm(atom.position - atoms[i].position) < 1.5:
    #             new_dex.append(atom.index)
    # longest_chain += new_dex
    # new_atoms = atoms[longest_chain]
    # write('water-chain.vasp', new_atoms)

    for atom in atoms:
        if atom.index in longest_chain:
            atom.symbol = 'C'
    write('water-chain.vasp', atoms)

def is_atom_in_cylinder(atom):
    cylinder_radius = 5  # Ångstrom
    cylinder_height = 16  # Ångstrom
    box_center_x = 15  # Ångstrom, half of 30 Å
    box_center_y = 15  # Ångstrom, half of 30 Å
    box_center_z = 20  # Ångstrom, half of 30 Å
    z_min = (box_center_z * 2 - cylinder_height) / 2  # Ångstrom, (40 - 20) / 2
    z_max = z_min + cylinder_height
    
    atom_position = atom.position
    
    distance_from_axis = np.linalg.norm(atom_position[:2] - np.array([box_center_x, box_center_y]))
    is_within_radius = distance_from_axis <= cylinder_radius
    is_within_height = z_min <= atom_position[2] <= z_max
    
    return is_within_radius and is_within_height

def water_chain(atoms, n):
    oxygen_indices = [o.index for o in atoms if o.symbol == 'O' and is_atom_in_cylinder(o)]    
    chains = [[i] for i in oxygen_indices]  # Initialize chains with individual oxygen atoms
    new_chains = chains
    i = 0
    
    while new_chains and i < n:
        i += 1
        print(f'Search water chains of length {i}')
        chains = new_chains
        new_chains = []
        for chain in chains:
            last_oxygen_index = chain[-1]
            for h in atoms:
                if h.symbol == 'H' and is_atom_in_cylinder(h):
                    if 0.8 < np.linalg.norm(atoms[last_oxygen_index].position - h.position) < 1.2:
                        for o in atoms:
                            if o.symbol == 'O' and is_atom_in_cylinder(o) and o.index not in chain \
                            and 1.5 < np.linalg.norm(h.position - o.position) < 2.5:
                                new_chain = chain + [o.index]
                                new_chains.append(new_chain)

    d_max = 0
    for chain in chains:
        d = np.linalg.norm(atoms[chain[0]].position - atoms[chain[-1]].position)
        if d > d_max:
            d_max = d
            longest_chain = chain
            
    return longest_chain

if __name__ == '__main__':
    main()