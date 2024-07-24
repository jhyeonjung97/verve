import os
import numpy as np
import pandas as pd

# Read input data
Ef_oxide = pd.read_csv('energy_norm_formation.tsv', delimiter='\t', index_col=0)
Ec_metal = pd.read_csv('/pscratch/sd/j/jiuy97/3_V_shape/6_Octahedral_RS/mendeleev_sublimation_heat.tsv', delimiter='\t', index_col=0)

# Fixed value for oxygen cohesive energy
Ec_oxygen = 5.1614  # eV

# Initialize an empty DataFrame for cohesive energy calculations
Ec_oxide = pd.DataFrame(index=Ef_oxide.index)
Ec_metal = pd.DataFrame(index=Ef_oxide.index)

print(Ec_metal)

# Determine the current working directory and perform calculations accordingly
current_dir = os.getcwd()

if '1_afm' in current_dir or '2_fm' in current_dir or '3d' in current_dir:
    Ec_oxide['energy'] = Ec_metal['3d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']
elif '4d' in current_dir:
    Ec_oxide['energy'] = Ec_metal['4d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']
elif '5d' in current_dir:
    Ec_oxide['energy'] = Ec_metal['5d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']
else:
    raise ValueError("The current directory does not match any expected pattern ('1_afm', '2_fm', '3d', '4d', '5d').")

# Save the calculated cohesive energies to a TSV file
Ec_oxide.to_csv('energy_norm_cohesive.tsv', sep='\t', index=True)
print("Cohesive energies of oxides calculated and saved to 'energy_norm_cohesive.tsv'.")
