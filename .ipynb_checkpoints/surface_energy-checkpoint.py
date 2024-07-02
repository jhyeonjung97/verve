import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse

coords = ['WZ', 'ZB', 'LT', 'TN', '33', 'RS']
coord_dirs = ['1_Tetrahedral_WZ', '2_Tetrahedral_ZB', '3_Pyramidal_LT',
                 '4_Square_Planar_TN', '5_Square_Planar_33', '6_Octahedral_RS']
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
markers = ['s', 'd', 'p', 'o', '>', '<', 'D']
stochiometris = [6, 6, 6, 8, 12, 8]
                 
metal_rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }
row_dirs = ['1_afm', '4d', '5d']

        
bulk_path = '/pscratch/sd/j/jiuy97/3_V_shape'
slab_path = '/pscratch/sd/j/jiuy97/4_V_slab'

for i in range(0, 6):
    coord = coords[i]
    coord_dir = coord_dirs[i]
    color = colors[i]
    marker = markers[i]
    stochiometry = stochiometris[i]
                 
    for j in rang(0, 3):
        metal_row = metal_rows[j]
        row_dir = row_dirs[j]
        dir_path = f'{coord_dir}/{row_dir}/'
        bulk_e_path = os.path.join(bulk_path, dir_path, 'energy_norm_energy.tsv')
        slab_e_path = os.path.join(slab_path, dir_path, 'energy_energy.tsv')
        area_e_path = os.path.join(slab_path, dir_path, 'energy_area.tsv')
        bulk_df = pd.read_csv(bulk_e_path, delimiter='\t').iloc[:, 1:]
        slab_df = pd.read_csv(slab_e_path, delimiter='\t').iloc[:, 1:]
        area_df = pd.read_csv(area_e_path, delimiter='\t').iloc[:, 1:]
        surface_df = (slab_df - stochiometry * bulk_df) / (2 * area_df)

        png_filename = f"formation_{row}.png"   
        tsv_filename = f"formation_{row}.tsv"

        plt.figure(figsize=(8, 6))

        for j, column in enumerate(df.columns):
            x = range(len(df[column]))
            filtered_df = df[column].dropna()
            if filtered_df.empty:
                print(f"No values found for pattern: {column}")
                continue
            plt.plot(x, filtered_df, marker=markers[j % len(markers)], color=colors[j % len(colors)], label=column)

        df.to_csv(tsv_filename, sep='\t')
        print(f"Merged data saved to {tsv_filename}")

        plt.xticks(np.arange(len(metal_rows[row])), metal_rows[row])
        plt.xlabel('Metal (MO)')
        plt.ylabel('Formation energy (eV/MO)')
        plt.legend()
        plt.tight_layout()
        plt.gcf().savefig(png_filename, bbox_inches="tight")
        print(f"Figure saved as {png_filename}")
        plt.close()