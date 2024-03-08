import os
import numpy as np
from sys import argv
from ase.io import read, write

file = argv[1]
print('file: ', file) #print
atoms = read(file)
name, ext = os.path.splitext(file)
print('file: ', name, ext) #print

print('len(argv): ', len(argv)) #print
if len(argv) < 3:
    print("No oxygen atom indices provided.")
    exit(1)

oxygen_indices = list(map(int, argv[2:]))
print('oxygen_indices: ', oxygen_indices) #print
for index in oxygen_indices:
    if atoms[index].symbol != 'O':
        print(f"This atom is not oxygen: {index}")
        exit(1)

for i in range(len(oxygen_indices) - 1):    
    oxygen1 = oxygen_indices[i]
    oxygen2 = oxygen_indices[i+1]
    hydrogen11 = None
    hydrogen21 = None
    hydrogen22 = None
    print(oxygen1, oxygen2) #print

    for atom in atoms:
        if atom.symbol == 'H':
            d1 = np.linalg.norm(atoms[oxygen1].position - atom.position)
            d2 = np.linalg.norm(atoms[oxygen2].position - atom.position)
            if 0.5 < d1 < 1.5:
                if hydrogen11 is None \
                or d1 < np.linalg.norm(atoms[oxygen1].position - atoms[hydrogen11].position):
                    hydrogen11 = atom.index
            if 0.5 < d2 < 1.5:
                if hydrogen21 is None:
                    hydrogen21 = atom.index
                elif hydrogen22 is None:
                    hydrogen22 = atom.index
    print(hydrogen11, hydrogen21, hydrogen22) #print

    if not hydrogen11:
        print(f"Not all required hydrogens were found near the oxygen atom: {oxygen1}")
        exit(1)
    if not hydrogen21 or not hydrogen22:
        print(f"Not all required hydrogens were found near the oxygen atom: {oxygen2}")
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
    print(O, M,
          A1, A2,
          B1, B2,
          C1, C2) #print

    d1 = np.linalg.norm(atoms[hydrogen11].position - B1)
    d2 = np.linalg.norm(atoms[hydrogen11].position - B2)
    if d1 < d2:
        atoms[hydrogen11].position = B1
    else:
        atoms[hydrogen11].position = B2
    print(hydrogen11, atoms[hydrogen11.position]) #print
    write(f'{name}_{i}{ext}', atoms)
