import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

coords = ['WZ', 'ZB', 'LT', 'TN', '33', 'RS']
coord_dirs = ['1_Tetrahedral_WZ', '2_Tetrahedral_ZB', '3_Pyramidal_LT',
              '4_Square_Planar_TN', '5_Square_Planar_33', '6_Octahedral_RS']
colors = ['#d62728', '#ff7f0e', '#ffd70e', '#2ca02c', '#279ff2', '#9467bd']
markers = ['s', 'd', 'p', 'o', '>', '<', 'D']
stochiometries = [6, 6, 6, 8, 12, 8]

rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
}
row_dirs = ['1_afm', '4d', '5d']

bulk_path = '/pscratch/sd/j/jiuy97/3_V_shape'
slab_path = '/pscratch/sd/j/jiuy97/4_V_slab'

for i in range(6):
    coord = coords[i]
    coord_dir = coord_dirs[i]
    color = colors[i]
    marker = markers[i]
    stochiometry = stochiometries[i]
    
    for j in range(3):
        row_key = list(rows.keys())[j]
        row = rows[row_key]
        row_dir = row_dirs[j]
        dir_path = f'{coord_dir}/{row_dir}/'
        bulk_e_path = os.path.join(bulk_path, dir_path, 'energy_norm_energy.tsv')
        slab_e_path = os.path.join(slab_path, dir_path, 'energy_energy.tsv')
        area_e_path = os.path.join(slab_path, dir_path, 'energy_area.tsv')
        
        if os.path.exists(bulk_e_path) and os.path.exists(slab_e_path) and os.path.exists(area_e_path):
            bulk_df = pd.read_csv(bulk_e_path, delimiter='\t').iloc[:, 1:]
            slab_df = pd.read_csv(slab_e_path, delimiter='\t').iloc[:, 1:]
            area_df = pd.read_csv(area_e_path, delimiter='\t').iloc[:, 1:]

            surface_df = pd.DataFrame(index=bulk_df.index, columns=bulk_df.columns)

            for k in range(len(bulk_df)):
                if not (pd.isna(slab_df.iloc[k, 0]) or pd.isna(bulk_df.iloc[k, 0]) or pd.isna(area_df.iloc[k, 0])):
                    surface_df.iloc[k, 0] = (slab_df.iloc[k, 0] - stochiometry * bulk_df.iloc[k, 0]) / (2 * area_df.iloc[k, 0])
                else:
                    surface_df.iloc[k, 0] = np.nan

            png_filename = f"surface_{coord}_{row_key}.png"
            tsv_filename = f"surface_{coord}_{row_key}.tsv"

            plt.figure(figsize=(8, 6))
        
            x = range(len(surface_df['energy']))
            filtered_df = surface_df['energy'].dropna()
            if filtered_df.empty:
                print(f"No values found for pattern: 'energy'")
                continue
            plt.plot(x, filtered_df, marker=marker, color=color, label=column)

            surface_df.to_csv(tsv_filename, sep='\t')
            print(f"Merged data saved to {tsv_filename}")

            plt.xticks(np.arange(len(row)), row)
            plt.xlabel('Metal (MO)')
            plt.ylabel('Surface energy (eV/A^2)')
            plt.legend()
            plt.tight_layout()
            plt.gcf().savefig(png_filename, bbox_inches="tight")
            print(f"Figure saved as {png_filename}")
            plt.close()