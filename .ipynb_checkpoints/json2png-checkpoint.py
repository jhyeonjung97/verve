from ase.io import read, write
import os
from ase.io.pov import get_bondpairs, set_high_bondorder_pairs
import matplotlib.pyplot as plt

coords = ['WZ', 'ZB', 'LT', 'TN', '33', 'RS']
coord_dirs = ['1_Tetrahedral_WZ', '2_Tetrahedral_ZB', '3_Pyramidal_LT',
              '4_Square_Planar_TN', '5_Square_Planar_33', '6_Octahedral_RS']
rotations = ['-90x,-90y,0z', '-90x,0y,0z', '-90x,-90y,0z', '-90x,-90y,0z', '-90x,-45y,0z', '-90x,-90y,0z']
repeats = [(1, 2, 1), (2, 1, 1), (1, 2, 1), (1, 2, 1), (1, 1, 1), (1, 1, 1)]
rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
}

slab_path = '/pscratch/sd/j/jiuy97/4_V_slab'

def render_pov(filename, atoms, rotation, radii, bondpairs):
    write(filename + '.pov', atoms, format='pov',
          radii=radii, rotation=rotation,
          povray_settings=dict(bondatoms=bondpairs))
    os.system(f"povray +I{filename}.pov +O{filename}.png +W800 +H600 +D +FN")

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
                    filename = f'{i}{coord}_{row_dir}_{k:02d}{metal}'
                    radii = [{'Ca': 0.5, 'Sc': 0.5, 'Ti': 0.5, 'V': 0.5, 'Cr': 0.5, 'Mn': 0.5, 'Fe': 0.5, 'Co': 0.5, 'Ni': 0.5, 'Cu': 0.5, 'Zn': 0.5, 'Ga': 0.5, 'Ge': 0.5,
                              'Sr': 0.5, 'Y': 0.5, 'Zr': 0.5, 'Nb': 0.5, 'Mo': 0.5, 'Tc': 0.5, 'Ru': 0.5, 'Rh': 0.5, 'Pd': 0.5, 'Ag': 0.5, 'Cd': 0.5, 'In': 0.5, 'Sn': 0.5,
                              'Ba': 0.5, 'La': 0.5, 'Hf': 0.5, 'Ta': 0.5, 'W': 0.5, 'Re': 0.5, 'Os': 0.5, 'Ir': 0.5, 'Pt': 0.5, 'Au': 0.5, 'Hg': 0.5, 'Tl': 0.5, 'Pb': 0.5}[at.symbol] for at in atoms]
                    bondpairs = get_bondpairs(atoms, radius=1.1)
                    high_bondorder_pairs = {}  # Define your high bond order pairs if needed
                    bondpairs = set_high_bondorder_pairs(bondpairs, high_bondorder_pairs)
                    render_pov(filename, atoms, rotation, radii, bondpairs)
                    print(f'Written: {filename}.png')
                except Exception as e:
                    print(f"Error writing {filename}: {e}")
