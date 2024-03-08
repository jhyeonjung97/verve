import os
import numpy as np
from sys import argv
from ase.io import read, write

file = argv[1]
atoms = read(file)
name, ext = os.path.splitext(file)

if len(argv) < 3:
    print("No oxygen atom indices provided.")
    exit(1)

oxygen_indices = list(map(int, argv[2:]))
for index in oxygen_indices:
    if atoms[index].symbol != 'O':
        print(f"This atom is not oxygen: {index}")
        exit(1)

for i in range(len(oxygen_indices) - 1):    
    oxygen1 = oxygen_indices[i]
    oxygen2 = oxygen_indices[i+1]
    hydrogen11 = None
    hydrogen12 = None
    hydrogen21 = None
    hydrogen22 = None

    for atom in atoms:
        if atom.symbol == 'H':
            d1 = np.linalg.norm(atoms[oxygen1].position - atom.position)
            d2 = np.linalg.norm(atoms[oxygen2].position - atom.position)
            if 0.5 < d1 < 1.5:
                if hydrogen11 is None:
                    hydrogen11 = atom.index
                elif hydrogen12 is None:
                    hydrogen12 = atom.index
                else:
                    print(f"Too many hydrogens {atom} were found near oxygen1: {oxygen1}")
            if 0.5 < d2 < 1.5:
                if hydrogen21 is None:
                    hydrogen21 = atom.index
                elif hydrogen22 is None:
                    hydrogen22 = atom.index
                elif atom.index == hydrogen:
                    continue
                else:
                    print(f"Too many hydrogens {atom} were found near oxygen2: {oxygen2}")
    
    d1 = np.linalg.norm(atoms[hydrogen11].position - atoms[oxygen2].position)
    d2 = np.linalg.norm(atoms[hydrogen12].position - atoms[oxygen2].position)
    if d1 < d2:
        hydrogen = hydrogen11
    else:
        hydrogen = hydrogen12
    print('hydrogen:', hydrogen) #print

    if hydrogen11 is None or hydrogen12 is None:
        print(f"Not all required hydrogens were found near the oxygen1: {oxygen1}")
        exit(1)
    if hydrogen21 is None or hydrogen22 is None:
        print(f"Not all required hydrogens were found near the oxygen2: {oxygen2}")
        exit(1)
                      
    O = atoms[oxygen2].position
    A1 = atoms[hydrogen21].position
    A2 = atoms[hydrogen22].position
    
    M = (A1 + A2) / 2
    B1 = np.cross(A1 - A2, O - M)
    B1 = B1 / np.linalg.norm(B1) * np.linalg.norm(A1 - M) + M
    B2 = 2 * M - B1
    C1 = 2 * O - B1
    C2 = 2 * O - B2
    print('O: ', O)
    print('M: ', M)
    print('A1: ', A1)
    print('A2: ', A2)
    print('B1: ', B1)
    print('B2: ', B2)
    print('C1: ', C1)
    print('C2: ', C2) #print

    d1 = np.linalg.norm(atoms[hydrogen].position - B1)
    d2 = np.linalg.norm(atoms[hydrogen].position - B2)
    if d1 < d2:
        atoms[hydrogen].position = B1
    else:
        atoms[hydrogen].position = B2
    write(f'{name}_{i}{ext}', atoms)
