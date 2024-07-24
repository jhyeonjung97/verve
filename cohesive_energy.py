import os
import numpy as np
import pandas as pd

Ef_oxide = pd.read_csv('energy_norm_formation.tsv', delimiter='\t', index_col=0)
Ec_metal = pd.read_csv('/pscratch/sd/j/jiuy97/3_V_shape/6_Octahedral_RS/mendeleev_sublimation_heat.tsv', delimiter='\t', index_col=0)

Ec_oxygen = 5.1614  # eV
Ec_oxide = pd.DataFrame(index=Ef_oxide.index)

if '1_afm' in os.getcwd() or '2_fm' in os.getcwd() or '3d' in os.getcwd():
    Ec_oxide['energy'] = Ec_metal['3d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']
elif '4d' in os.getcwd():
    Ec_oxide['energy'] = Ec_metal['4d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']
elif '5d' in os.getcwd():
    Ec_oxide['energy'] = Ec_metal['5d'] / 96.48 + Ec_oxygen - Ef_oxide['energy']

Ec_oxide.to_csv('energy_norm_cohesive.tsv', sep='\t', index=True)
print("Cohesive energies of oxides calculated and saved to 'energy_norm_cohesive.tsv'.")