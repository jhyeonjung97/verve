import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

metal_rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }

nist = {
    'Ti': {'M': 1, 'O': 2, 'G_form': -889.406}, # 1692 1809 mp-2657 Titanium Dioxide (Rutile)
    'V': {'M': 2, 'O': 5, 'G_form': -1419.359}, # 1780 1892 mp-25279 Divanadium Pentaoxide
    'Cr': {'M': 2, 'O': 3, 'G_form': -1058.067}, # 573 688 mp-19399 Dichromium Trioxide
    'Mn': {'M': 1, 'O': 1, 'G_form': -362.898}, # 1046 1162 mp-19006 Manganese Oxide
    'Fe': {'M': 2, 'O': 3, 'G_form': -742.294}, # 702 817 mp-19770 Hematite
    'Co': {'M': 3, 'O': 4, 'G_form': -794.901}, # 544 659 mp-18748 Tricobalt Tetraoxide
    'Ni': {'M': 1, 'O': 1, 'G_form': -211.539}, # 1213 1330 mp-19009 Nickel Oxide
    'Cu': {'M': 1, 'O': 1, 'G_form': -128.292}, # 620 735 mp-704645 Copper Monoxide
    }

metal_path = '/pscratch/sd/j/jiuy97/3_V_shape/metal/0_min/energy_norm.tsv'
oxide_path = '/pscratch/sd/j/jiuy97/3_V_shape/oxide/0_min/energy_norm.tsv'
path = '/pscratch/sd/j/jiuy97/3_V_shape/metal/merged_norm_energy.tsv'

metal_df = pd.read_csv(metal_path, delimiter='\t').iloc[:, 1:]
oxide_df = pd.read_csv(oxide_path, delimiter='\t').iloc[:, 1:]
df = pd.read_csv(path, delimiter='\t').iloc[:, 1:]

metal_df.index = list(nist.keys())
oxide_df.index = list(nist.keys())
df.index = metal_rows['3d']

min_values = df.iloc[:, :3].min(axis=1)
df = df.iloc[:, 3:]

E_O2 = -8.7702210 # eV, DFT
TS_O2 = 0.635139 # eV, at 298.15 K, 1 atm
ZPE_O2 = 0.096279 # eV, at 298.15 K, 1 atm
E_oxygen = E_O2 /2
G_oxygen = (E_O2 - TS_O2 + ZPE_O2) / 2

for element, data in nist.items():
    data['G_form'] = data['G_form'] / data['M'] / 96.48
    data['OtoM'] = data['O'] / data['M']
    data['G_oxide'] = oxide_df.loc[element, 'energy'] - oxide_df.loc[element, 'TS'] + oxide_df.loc[element, 'ZPE']
    data['G_metal'] = data['G_oxide'] - data['G_form'] - data['OtoM'] * G_oxygen
    data['E_metal'] = data['G_metal'] + metal_df.loc[element, 'TS'] - metal_df.loc[element, 'ZPE']

for i, metal in enumerate(metal_rows['3d']):
    if metal in nist:
        min_values.loc[metal] = nist[metal]['E_metal']
df.insert(0, '3d', min_values)

energy_path = './energy_norm_energy.tsv'
if not os.path.exists(energy_path):
    exit(1)
else:
    energy_df = pd.read_csv(energy_path, delimiter='\t', index_col=0)
    formation = pd.DataFrame(index=energy_df.index, columns=energy_df.columns)

for row in metal_rows:
    if metal_rows[row] == energy_df.index.tolist():
        formation = energy_df.sub(df[row].values, axis=0) - E_oxygen

plt.figure(figsize=(8, 6))
png_filename = f"energy_norm_formation.png"   
tsv_filename = f"energy_norm_formation.tsv"

colors = plt.cm.rainbow(np.linspace(0, 1, len(formation.columns))) 

for j, column in enumerate(formation.columns):
    x = range(len(formation[column]))
    filtered_df = formation[column]
    # filtered_df = formation[column].dropna()
    if filtered_df.empty:
        print(f"No values found for pattern: {column}")
        continue
    print(x)
    print(filtered_df)
    plt.plot(x, filtered_df, marker='o', color=colors[j % len(colors)], label=column)

formation.to_csv(tsv_filename, sep='\t')
print(f"Merged data saved to {tsv_filename}")

plt.xticks(x, formation.index)
plt.xlabel('Metal (MO)')
plt.ylabel('Formation energy (eV/MO)')
plt.legend()
plt.tight_layout()
plt.gcf().savefig(png_filename, bbox_inches="tight")
print(f"Figure saved as {png_filename}")
plt.close()