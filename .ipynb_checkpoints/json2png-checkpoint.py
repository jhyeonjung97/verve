from ase.io import read, write
import os

coords = ['WZ', 'ZB', 'LT', 'TN', '33', 'RS']
coord_dirs = ['1_Tetrahedral_WZ', '2_Tetrahedral_ZB', '3_Pyramidal_LT',
              '4_Square_Planar_TN', '5_Square_Planar_33', '6_Octahedral_RS']

rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
}

slab_path = '/pscratch/sd/j/jiuy97/4_V_slab'

for i in range(6):
    coord = coords[i]
    coord_dir = coord_dirs[i]
    
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

            if atoms:
                try:
                    filename = f'{i}_{coord}_{row_dir}_{k:02d}_{metal}.png'
                    write(filename, atoms, rotation=('0x,0y,0z'), show_unit_cell=True)
                    print(f'Written: {filename}')
                except Exception as e:
                    print(f"Error writing {filename}: {e}")
