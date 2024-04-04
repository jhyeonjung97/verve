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

oxygen_E = -8.7702210 # eV, DFT
oxygen_TS = 0.635139 # eV, at 298.15 K, 1 atm
oxygen_ZPE = 0.096279 # eV, at 298.15 K, 1 atm
oxygen = (oxygen_E - oxygen_TS + oxygen_ZPE) / 2

nist = {
    'Ti': {'M': 1, 'O':2, 'H_form': -944.747, 'G_form': -889.406, 'E_dft': -99.45192424}, 
    #, 'ZPE': , 'S_vib': }, # 1692 1809 mp-2657 Titanium Dioxide (Rutile)
    'V': {'M': 2, 'O':5, 'H_form': -1550.59, 'G_form': -1419.359, 'E_dft': -104.1937574}, 
    #, 'ZPE': , 'S_vib': }, # 1780 1892 mp-25279 Divanadium Pentaoxide
    'Cr': {'M': 2, 'O':3, 'H_form': -1139.701, 'G_form': -1058.067, 'E_dft': -79.58654325}, 
    #, 'ZPE': , 'S_vib': }, # 573 688 mp-19399 Dichromium Trioxide
    'Mn': {'M': 1, 'O':1, 'H_form': -385.221, 'G_form': -362.898, 'E_dft': -31.17185317}, 
    #, 'ZPE': , 'S_vib': }, # 1046 1162 mp-19006 Manganese Oxide
    'Fe': {'M': 2, 'O':3, 'H_form': -824.248, 'G_form': -742.294, 'E_dft': -68.25294948}, 
    #, 'ZPE': , 'S_vib': }, # 702 817 mp-19770 Hematite
    'Co': {'M': 3, 'O':4, 'H_form': -910.020, 'G_form': -794.901, 'E_dft': -84.1526723}, 
    #, 'ZPE': , 'S_vib': }, # 544 659 mp-18748 Tricobalt Tetraoxide
    'Ni': {'M': 1, 'O':1, 'H_form': -239.701, 'G_form': -211.539, 'E_dft': -20.40998666}, 
    #, 'ZPE': , 'S_vib': }, # 1213 1330 mp-19009 Nickel Oxide
    'Cu': {'M': 1, 'O':1, 'H_form': -156.063, 'G_form': -128.292, 'E_dft': -17.83506218} 
    #, 'ZPE': , 'S_vib': } # 620 735 mp-704645 Copper Monoxide
    }

T = 298.15
for element, data in nist.items():
    # G_oxide = nist[element]['E_dft'] - T * nist[element]['S_vib'] + nist[element]['ZPE']
    # G_formation = nist[element]['G_form']
    # nist.add(element['metal']) = G_oxide - G_formation - oxygen
    nist[element]['E_metal'] = (data['E_dft'] - data['H_form'] - (data['O'] * oxygen_E)) / data['M']
    
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