import os
import numpy as np
import pandas as pd

# Read input data
Ef_oxide = pd.read_csv('energy_norm_formation.tsv', delimiter='\t', index_col=0)
Ec_metal = pd.read_csv('/pscratch/sd/j/jiuy97/3_V_shape/6_Octahedral_RS/mendeleev_sublimation_heat.tsv', delimiter='\t', index_col=0)

rows = {
    '3d': ['Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge'],
    '4d': ['Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn'],
    '5d': ['Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb']
    }

# Fixed value for oxygen cohesive energy
Ec_oxygen = 5.1614  # eV

# Initialize an empty DataFrame for cohesive energy calculations
Ec_oxide = pd.DataFrame(index=Ef_oxide.index)
Ec_metal.index = Ef_oxide.index

# Determine the current working directory and perform calculations accordingly
current_dir = os.getcwd()

if '1_afm' in current_dir or '2_fm' in current_dir or '3d' in current_dir:
    row = '3d'
elif '4d' in current_dir:
    row = '4d'
elif '5d' in current_dir:
    row = '5d'
    
Ec_oxide['energy'] = Ec_metal[row] / 96.48 + Ec_oxygen / 2 - Ef_oxide['energy']

# Save the calculated cohesive energies to a TSV file
Ec_oxide.to_csv('energy_norm_cohesive.tsv', sep='\t', index=True)
print(f"Data saved to energy_norm_cohesive.tsv")

if '1_Tetrahedral_WZ' in current_dir:
    marker = '>'; color = '#d62728'
elif '2_Tetrahedral_ZB' in current_dir:
    marker = '<'; color = '#ff7f0e'
elif '3_Tetragonal_LT' in current_dir:
    marker = 'o'; color = '#ffd70e'
elif '4_Square_Planar_TN' in current_dir:
    marker = 's'; color = '#2ca02c'
elif '5_Square_Planar_NB' in current_dir:
    marker = 'p'; color = '#279ff2'
elif '6_Octahedral_RS' in current_dir:
    marker = 'd'; color = '#9467bd'
else:
    marker = 'x'; color = 'k'
        
plt.figure(figsize=(10, 6))
x = []
filtered_values = []
for i, v in enumerate(Ec_oxide['energy']):
    if not np.isnan(v): 
        x.append(i)
        filtered_values.append(v)
plt.plot(x, Ec_oxide['energy'], marker=marker, color=color)
plt.xlabel('Metal (MO)')
plt.ylabel('Cohesive energy (eV)')
plt.xticks(np.arange(len(dir_names)), dir_names)
plt.tight_layout()
if save:
    png_filename = f"{filename}_{pattern}.png"            
    plt.savefig(png_filename, bbox_inches="tight")
    plt.close()
    print(f"Figure saved as {png_filename}")
else:
    plt.show()