import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

metal_rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }

metal_path = '/pscratch/sd/j/jiuy97/3_V_shape/metal/merged_norm_energy.tsv'
metal_df = pd.read_csv(metal_path, delimiter='\t').iloc[:, 1:]
min_values = metal_df.iloc[:, :3].min(axis=1)

oxygen_E = -8.7702210 # eV, DFT
oxygen_TS = 0.635139 # eV, at 298.15 K, 1 atm
oxygen_ZPE = 0.096279 # eV, at 298.15 K, 1 atm
oxygen = (oxygen_E - oxygen_TS + oxygen_ZPE) / 2

metal_df.drop(metal_df.columns[:3], axis=1, inplace=True)
metal_df.insert(0, '3d', min_values)

for row in metal_rows:
    oxide_path = './energy_norm_energy.tsv'
    oxide_df = pd.read_csv(oxide_path, delimiter='\t', index_col=0)
    if metal_rows[row] == oxide_df.index.tolist():
        df = oxide_df.sub(metal_df[row].values, axis=0) - oxygen

plt.figure(figsize=(8, 6))
png_filename = f"energy_formation.png"   
tsv_filename = f"energy_formation.tsv"

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