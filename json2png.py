from ase.io import read
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

coords = ['WZ', 'ZB', 'LT', 'TN', '33', 'RS']
coord_dirs = ['1_Tetrahedral_WZ', '2_Tetrahedral_ZB', '3_Pyramidal_LT',
              '4_Square_Planar_TN', '5_Square_Planar_33', '6_Octahedral_RS']
# rotations = ['-90x,-90y,0z', '-90x,0y,0z', '-90x,-90y,0z', '-90x,-90y,0z', '-90x,-45y,0z', '-90x,-90y,0z']
rotations = ['-90,-90', '-90,0', '-90,-90', '-90,-90', '-90,-45', '-90,-90']
repeats = [(1, 2, 1), (2, 1, 1), (1, 2, 1), (1, 2, 1), (1, 1, 1), (1, 1, 1)]
rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
}

slab_path = '/pscratch/sd/j/jiuy97/4_V_slab'

def compute_bondpairs(atoms, max_distance=1.1):
    positions = atoms.get_positions()
    bondpairs = []
    for i, pos_i in enumerate(positions):
        for j, pos_j in enumerate(positions):
            if i < j:
                distance = np.linalg.norm(pos_i - pos_j)
                if distance <= max_distance:
                    bondpairs.append((i, j))
    return bondpairs

def plot_atoms(atoms, filename, rotation):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot atoms
    for atom in atoms:
        ax.scatter(atom.position[0], atom.position[1], atom.position[2], s=100, label=atom.symbol)

    # Plot bonds
    bondpairs = compute_bondpairs(atoms)
    for (i, j) in bondpairs:
        ax.plot([atoms[i].position[0], atoms[j].position[0]],
                [atoms[i].position[1], atoms[j].position[1]],
                [atoms[i].position[2], atoms[j].position[2]], 'k-')

    # Set rotation
    elev, azim = map(float, rotation.split(','))
    ax.view_init(elev=elev, azim=azim)

    plt.savefig(filename)
    plt.close(fig)

for i in range(6):
    coord = coords[i]
    coord_dir = coord_dirs[i]
    rotation = rotations[i]
    repeat = repeats[i]
    
    for j in range(3):
        row_dir = list(rows.keys())[j]
        row = rows[row_dir]
    
        for k in range(13):
            metal = row[k]
            metal_dir = f'{k:02d}_{metal}'
            metal_x_dir = f'{k:02d}x_{metal}'
            dir_path = f'{slab_path}/{coord_dir}/{row_dir}/{metal_dir}'
            dir_x_path = f'{slab_path}/{coord_dir}/{row_dir}/{metal_x_dir}'

            atoms = None
            if os.path.exists(f'{dir_path}/restart.json'):
                atoms = read(f'{dir_path}/restart.json')
            elif os.path.exists(f'{dir_x_path}/restart.json'):
                atoms = read(f'{dir_x_path}/restart.json')
            elif os.path.exists(f'{dir_x_path}/CONTCAR'):
                atoms = read(f'{dir_x_path}/CONTCAR')
            elif os.path.exists(f'{dir_x_path}/start.traj'):
                atoms = read(f'{dir_x_path}/start.traj')
            else:
                print(f'There is no structure file in directory: {dir_path}')
                continue
    
            atoms = atoms.repeat(repeat)

            if atoms:
                try:
                    filename = f'{i}{coord}_{row_dir}_{k:02d}{metal}.png'
                    plot_atoms(atoms, filename, rotation)
                    print(f'Written: {filename}')
                except Exception as e:
                    print(f"Error writing {filename}: {e}")
