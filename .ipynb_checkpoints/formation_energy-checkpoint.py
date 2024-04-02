import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

metal_rows = {
    '3d_afm': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '3d_fm': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }

combined_labels = [f'{a}\n{b}\n{c}' for a, b, c in zip(metal_rows['3d'], metal_rows['4d'], metal_rows['5d'])]

metal_path = '/pscratch/sd/j/jiuy97/3_V_shape/metal/merged_norm_energy.tsv'
metal_df = pd.read_csv(metal_path, delimiter='\t').iloc[:, 1:]
min_values = metal_df.iloc[:, :3].min(axis=1)

oxygen_E = -8.7702210 # eV, DFT
oxygen_TS = 0.635139 # eV, at 298.15 K, 1 atm
oxygen_ZPE = 0.096279 # eV, at 298.15 K, 1 atm
oxygen = (oxygen_E - oxygen_TS + oxygen_ZPE) / 2

# metal_3d = ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
# nist = {
#     'Ti': {'M': 1, 'O':2, 'Ef': -889.406, 'E_dft': , 'ZPE': , 'S_vib': }, # 1692 1809 mp2657 Titanium Dioxide (Rutile)
#     'V': {'M': 2, 'O':5, 'Ef': -1419.359, 'E_dft': , 'ZPE': , 'S_vib': }, # 1780 1892 mp25279 Divanadium Pentaoxide
#     'Cr': {'M': 2, 'O':3, 'Ef': -1058.067, 'E_dft': , 'ZPE': , 'S_vib': }, # 573 688 mp19399 Dichromium Trioxide
#     'Mn': {'M': 1, 'O':1, 'Ef': -362.898, 'E_dft': , 'ZPE': , 'S_vib': }, # 1046 1162 mp19006 Manganese Oxide
#     'Fe': {'M': 2, 'O':3, 'Ef': -742.294, 'E_dft': , 'ZPE': , 'S_vib': }, # 702 817 mp19770 Hematite
#     'Co': {'M': 3, 'O':4, 'Ef': -794.901, 'E_dft': , 'ZPE': , 'S_vib': }, # 544 659 mp18748 Tricobalt Tetraoxide
#     'Ni': {'M': 1, 'O':1, 'Ef': -211.539, 'E_dft': , 'ZPE': , 'S_vib': }, # 1213 1330 mp19009 Nickel Oxide
#     'Cu': {'M': 1, 'O':1, 'Ef': -128.292, 'E_dft': , 'ZPE': , 'S_vib': } # 620 735 mp704645 Copper Monoxide
#     }

# T = 298.15
# for element in nist:
#     G_oxide = nist[element]['E_dft'] - T * nist[element]['S_vib'] + nist[element]['ZPE']
#     G_formation = nist[element]['Ef']
#     nist.add(element['metal']) = G_oxide - G_formation - oxygen
    
# for i, metal in enumerate(metal_3d):
#     if metal in ['Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu']:
#         min_values[i] = nist[metal]['metal']

metal_df.drop(metal_df.columns[:3], axis=1, inplace=True)
metal_df.insert(0, '3d', min_values)
metal_df.insert(0, '3d_fm', min_values)
metal_df.insert(0, '3d_afm', min_values)

colors = ['#d62728', '#ff7f0e', '#2ca02c', '#279ff2', '#9467bd']
markers = ['s', 'd', 'p', 'o', '>', '<', 'D']

rows = ['3d_afm', '3d_fm', '3d', '4d', '5d']
for row in rows:
    oxide_path = f'/pscratch/sd/j/jiuy97/3_V_shape/merged_norm_energy_{row}.tsv'
    oxide_df = pd.read_csv(oxide_path, delimiter='\t').iloc[:, 1:]
    df = oxide_df.sub(metal_df[row].values, axis=0) - oxygen
    png_filename = f"formation_{row}.png"   
    tsv_filename = f"formation_{row}.tsv"
    
    plt.figure(figsize=(8, 6))
    # reversed_filenames = reversed(filenames)
    # reversed_labels = reversed(labels)
    # reversed_colors = reversed(colors)
    # reversed_markers = reversed(markers)
    
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


