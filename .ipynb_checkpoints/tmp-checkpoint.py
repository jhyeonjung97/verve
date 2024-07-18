import numpy as np
import pandas as pd

# Load the data from TSV files
# concat_norm_formation.tsv contains formation energies
# concat_sublimation_heat.tsv contains sublimation heats (or cohesive energies) of metals
Ef_oxide = pd.read_csv('concat_norm_formation.tsv', delimiter='\t', index_col=0)
Ec_metal = pd.read_csv('concat_sublimation_heat.tsv', delimiter='\t', index_col=0)

# Cohesive energy of O2 molecule (converted to eV/atom)
Ec_oxygen = 5.1614  # eV

# Calculate cohesive energy of oxides
# Note: Conversion from kJ/mol to eV (1 eV = 96.485 kJ/mol)
Ec_oxide = Ec_metal / 96.485 + Ec_oxygen - Ef_oxide

# Save the result to a TSV file
Ec_oxide.to_csv('concat_norm_cohesive.tsv', sep='\t', index=True)

print("Cohesive energies of oxides calculated and saved to 'concat_norm_cohesive.tsv'.")
