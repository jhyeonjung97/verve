import numpy as np
from ase.io import read

### READ DOSCAR ###
def read_dosfile():
    with open("DOSCAR", 'r') as f:
        lines = f.readlines()
    index = 0
    natoms = int(lines[index].strip().split()[0])
    index = 5
    nedos = int(lines[index].strip().split()[2])
    efermi = float(lines[index].strip().split()[3])
    print(natoms, nedos, efermi)

    return lines, index, natoms, nedos, efermi

### READ POSCAR or CONTCAR and save pos
def read_posfile():
    try:
        atoms = read('POSCAR')
    except IOError:
        print("[__main__]: Couldn't open input file POSCAR, atomic positions will not be written...\n")
        atoms = []

    return atoms

### WRITE DOS0 CONTAINING TOTAL DOS ###
def write_dos0(lines, index, nedos, efermi):

    with open("DOS0", 'w') as fdos:
        line = lines[index+1].strip().split()
        ncols = len(line)

        for n in range(nedos):
            index += 1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi
            fdos.write(f'{e_f:15.8f} ')

            for col in range(1, ncols):
                dos = float(lines[index].strip().split()[col])
                fdos.write(f'{dos:15.8f} ')
            fdos.write('\n')
    return index

### LOOP OVER SETS OF DOS, NATOMS ###
def write_nospin(lines, index, nedos, natoms, ncols, efermi):

    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    for i in range(1, natoms + 1):
        si = str(i)

        ## OPEN DOSi FOR WRITING ##
        with open("DOS" + si, 'w') as fdos:
            index += 1
            ia = i - 1
            fdos.write(f'# {pos[ia,0]:15.8f} {pos[ia,1]:15.8f} {pos[ia,2]:15.8f} \n')

            ### LOOP OVER NEDOS ###
            for n in range(nedos):
                index += 1
                e = float(lines[index].strip().split()[0])
                e_f = e - efermi
                fdos.write(f'{e_f:15.8f} ')

                for col in range(1, ncols):
                    dos = float(lines[index].strip().split()[col])
                    fdos.write(f'{dos:15.8f} ')
                fdos.write('\n')

def write_spin(lines, index, nedos, natoms, ncols, efermi):
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    nsites = (ncols - 1) // 2

    for i in range(1, natoms + 1):
        si = str(i)

        ## OPEN DOSi FOR WRITING ##
        with open("DOS" + si, 'w') as fdos:
            index += 1
            ia = i - 1
            fdos.write(f'# {ncols} \n')
            fdos.write(f'# {pos[ia,0]:15.8f} {pos[ia,1]:15.8f} {pos[ia,2]:15.8f} \n')

            ### LOOP OVER NEDOS ###
            for n in range(nedos):
                index += 1
                e = float(lines[index].strip().split()[0])
                e_f = e - efermi
                fdos.write(f'{e_f:15.8f} ')

                for site in range(nsites):
                    dos_up = float(lines[index].strip().split()[site * 2 + 1])
                    dos_down = float(lines[index].strip().split()[site * 2 + 2]) * -1
                    fdos.write(f'{dos_up:15.8f} {dos_down:15.8f} ')
                fdos.write('\n')

#
if __name__ == '__main__':
    import sys
    import os
    import datetime
    import time
    import optparse

    lines, index, natoms, nedos, efermi = read_dosfile()
    index = write_dos0(lines, index, nedos, efermi)
    ## Test if a spin polarized calculation was performed ##
    line = lines[index+2].strip().split()
    ncols = len(line)
    if ncols in [7, 19, 9, 33]:
        write_spin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = True
    else:
        write_nospin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = False
    print("Spin unrestricted calculation:", is_spin)
