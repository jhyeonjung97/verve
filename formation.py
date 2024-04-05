import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

metal_rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'H_form', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }

metal_path = '/pscratch/sd/j/jiuy97/3_V_shape/metal/merged_norm_energy.tsv'
metal_df = pd.read_csv(metal_path, delimiter='\t').iloc[:, 1:]
min_values = metal_df.iloc[:, :3].min(axis=1)

E_O2 = -8.7702210 # eV, DFT
TS_O2 = 0.635139 # eV, at 298.15 K, 1 atm
ZPE_O2 = 0.096279 # eV, at 298.15 K, 1 atm
G_oxygen = (E_O2 - TS_O2 + ZPE_O2) / 2

nist = {
    'Ti': {'M_oxide': 4, 'O_oxide': 8, 'H_form': -944.747, 'G_form': -889.406, 
           'E_oxide': -99.45192424}, 'ZPE_oxide': 0.767633, 'TS_oxide': 0.565118}, 
          # 1692 1809 mp-2657 Titanium Dioxide (Rutile)
    'V': {'M_oxide': 4, 'O_oxide': 10, 'H_form': -1550.59, 'G_form': -1419.359, 
          'E_oxide': -104.1937574, 'ZPE_oxide': 1.006188, 'TS_oxide': 0.737889}, 
          # 1780 1892 mp-25279 Divanadium Pentaoxide
    'Cr': {'M_oxide': 4, 'O_oxide': 6, 'H_form': -1139.701, 'G_form': -1058.067, 
           'E_oxide': -79.58654325, 'ZPE_oxide': 0.736283, 'TS_oxide': 0.319027}, 
          # 573 688 mp-19399 Dichromium Trioxide
    'Mn': {'M_oxide': 2, 'O_oxide': 2, 'H_form': -385.221, 'G_form': -362.898, 
           'E_oxide': -31.17185317, 'ZPE_oxide': 0.141579, 'TS_oxide': 0.217217}, 
          # 1046 1162 mp-19006 Manganese Oxide
    'Fe': {'M_oxide': 4, 'O_oxide': 6, 'H_form': -824.248, 'G_form': -742.294, 
           'E_oxide': -68.25294948, 'ZPE_oxide': 0.614555, 'TS_oxide': 0.435567}, 
          # 702 817 mp-19770 Hematite
    'Co': {'M_oxide': 6, 'O_oxide': 8, 'H_form': -910.020, 'G_form': -794.901, 
           'E_oxide': -84.1526723, 'ZPE_oxide': 0.741766, 'TS_oxide': 0.778022}, 
          # 544 659 mp-18748 Tricobalt Tetraoxide
    'Ni': {'M_oxide': 1, 'O_oxide': 1, 'H_form': -239.701, 'G_form': -211.539, 
           'E_oxide': -20.40998666, 'ZPE_oxide': 0.185629, 'TS_oxide': 0.158862}, 
          # 1213 1330 mp-19009 Nickel Oxide
    'Cu': {'M_oxide': 2, 'O_oxide': 2, 'H_form': -156.063, 'G_form': -128.292, 
           'E_oxide': -17.83506218, 'ZPE_oxide': 0.202626, 'TS_oxide': 0.155208} 
          # 620 735 mp-704645 Copper Monoxide
    }

for element, data in nist.items():
    data['H_form'] = data['H_form'] / 96.48
    data['G_form'] = data['G_form'] / 96.48
    data['G_oxide'] = data['E_oxide'] - data['TS_oxide'] + data['ZPE_oxide']
    data['G_metal'] = (data['G_oxide'] - data['G_form'] - (data['O'] * G_oxygen)) / data['M']
    data['E_metal'] = data['G_metal'] + data['TS_metal'] - data['ZPE_metal']
    
print(nist)
    
for i, metal in enumerate(metal_rows['3d']):
    if metal in nist:
        min_values[i] = nist[metal]['E_metal']

print(min_values)

for row in metal_rows:
    oxide_path = './energy_norm_energy.tsv'
    oxide_df = pd.read_csv(oxide_path, delimiter='\t', index_col=0)
    if metal_rows[row] == oxide_df.index.tolist():
        df = oxide_df.sub(metal_df[row].values, axis=0) - oxygen

plt.figure(figsize=(8, 6))
png_filename = f"energy_norm_formation.png"   
tsv_filename = f"energy_norm_formation.tsv"

colors = plt.cm.rainbow(np.linspace(0, 1, len(df.columns))) 

for j, column in enumerate(df.columns):
    x = range(len(df[column]))
    filtered_df = df[column].dropna()
    if filtered_df.empty:
        print(f"No values found for pattern: {column}")
        continue
    plt.plot(x, filtered_df, marker='o', color=colors[j % len(colors)], label=column)

df.to_csv(tsv_filename, sep='\t')
print(f"Merged data saved to {tsv_filename}")

plt.xticks(x, df.index)
plt.xlabel('Metal (MO)')
plt.ylabel('Formation energy (eV/MO)')
plt.legend()
plt.tight_layout()
plt.gcf().savefig(png_filename, bbox_inches="tight")
print(f"Figure saved as {png_filename}")
plt.close()